import os
import shutil
import nltk
from whisperx.alignment import DEFAULT_ALIGN_MODELS_HF, DEFAULT_ALIGN_MODELS_TORCH
import logging
from whisperx.utils import LANGUAGES, TO_LANGUAGE_CODE

punct_model_langs = [
    "en",
    "fr",
    "de",
    "es",
    "it",
    "nl",
    "pt",
    "bg",
    "pl",
    "cs",
    "sk",
    "sl",
]
wav2vec2_langs = list(DEFAULT_ALIGN_MODELS_TORCH.keys()) + list(
    DEFAULT_ALIGN_MODELS_HF.keys()
)

whisper_langs = sorted(LANGUAGES.keys()) + sorted(
    [k.title() for k in TO_LANGUAGE_CODE.keys()]
)


# def create_config(output_dir):
#     # Can be meeting, telephonic, or general based on domain type of the audio
#     # file
#     DOMAIN_TYPE = "telephonic"
#     CONFIG_LOCAL_DIRECTORY = "nemo_msdd_configs"
#     CONFIG_FILE_NAME = f"diar_infer_{DOMAIN_TYPE}.yaml"
#     MODEL_CONFIG_PATH = os.path.join(CONFIG_LOCAL_DIRECTORY, CONFIG_FILE_NAME)
#     if not os.path.exists(MODEL_CONFIG_PATH):
#         os.makedirs(CONFIG_LOCAL_DIRECTORY, exist_ok=True)
#         CONFIG_URL = (
#             f"https://raw.githubusercontent.com/NVIDIA/NeMo/main/"
#             f"examples/speaker_tasks/diarization/conf/inference/"
#             f"{CONFIG_FILE_NAME}"
#         )
#         MODEL_CONFIG_PATH = wget.download(CONFIG_URL, MODEL_CONFIG_PATH)

#     config = OmegaConf.load(MODEL_CONFIG_PATH)

#     data_dir = os.path.join(output_dir, "data")
#     os.makedirs(data_dir, exist_ok=True)

#     meta = {
#         "audio_filepath": os.path.join(output_dir, "mono_file.wav"),
#         "offset": 0,
#         "duration": None,
#         "label": "infer",
#         "text": "-",
#         "rttm_filepath": None,
#         "uem_filepath": None,
#     }
#     with open(os.path.join(data_dir, "input_manifest.json"), "w") as fp:
#         json.dump(meta, fp)
#         fp.write("\n")

#     pretrained_vad = "vad_multilingual_marblenet"
#     pretrained_speaker_model = "titanet_large"
#     config.num_workers = 0
#     config.diarizer.manifest_filepath = os.path.join(data_dir, "input_manifest.json")
#     config.diarizer.out_dir = (
#         output_dir  # Directory to store intermediate files and prediction outputs
#     )

#     config.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
#     config.diarizer.oracle_vad = (
#         False  # compute VAD provided with model_path to vad config
#     )
#     config.diarizer.clustering.parameters.oracle_num_speakers = False

#     # Here, we use our in-house pretrained NeMo VAD model
#     config.diarizer.vad.model_path = pretrained_vad
#     config.diarizer.vad.parameters.onset = 0.8
#     config.diarizer.vad.parameters.offset = 0.6
#     config.diarizer.vad.parameters.pad_offset = -0.05
#     config.diarizer.msdd_model.model_path = (
#         "diar_msdd_telephonic"  # Telephonic speaker diarization model
#     )

#     return config


def get_word_ts_anchor(s, e, option="start"):
    if option == "end":
        return e
    elif option == "mid":
        return (s + e) / 2
    return s


def get_words_speaker_mapping(wrd_ts, spk_ts, word_anchor_option="start"):
    s, e, sp = spk_ts[0]
    wrd_pos, turn_idx = 0, 0
    wrd_spk_mapping = []
    for wrd_dict in wrd_ts:
        ws, we, wrd = (
            int(wrd_dict["start"] * 1000),
            int(wrd_dict["end"] * 1000),
            wrd_dict["word"],
        )
        wrd_pos = get_word_ts_anchor(ws, we, word_anchor_option)
        while wrd_pos > float(e):
            turn_idx += 1
            turn_idx = min(turn_idx, len(spk_ts) - 1)
            s, e, sp = spk_ts[turn_idx]
            if turn_idx == len(spk_ts) - 1:
                e = get_word_ts_anchor(ws, we, option="end")
        wrd_spk_mapping.append(
            {"word": wrd, "start_time": ws, "end_time": we, "speaker": sp}
        )
    return wrd_spk_mapping


sentence_ending_punctuations = ".?!"


def get_first_word_idx_of_sentence(word_idx, word_list, speaker_list, max_words):
    """This function returns the index of the first word of the sentence that contains the word at word_index.

    Args:
        word_idx (int): Index of the word in the word_list.
        word_list (list): List of words.
        speaker_list (list): List of speakers.
        max_words (int): Maximum number of words in a sentence.

    Returns:
        int: Index of the first word of the sentence that contains the word at word_index.
    """
    def is_word_sentence_end(x):
        return x >= 0 and word_list[x][-1] in sentence_ending_punctuations

    left_idx = word_idx
    while (
        left_idx > 0
        and word_idx - left_idx < max_words
        and speaker_list[left_idx - 1] == speaker_list[left_idx]
        and not is_word_sentence_end(left_idx - 1)
    ):
        left_idx -= 1

    return left_idx if left_idx == 0 or is_word_sentence_end(left_idx - 1) else -1


def get_last_word_idx_of_sentence(word_idx, word_list, max_words):
    """This function returns the index of the last word of the sentence that contains the word at word_index.

    Args:
        word_idx (int): Index of the word in the word_list.
        word_list (list): List of words.
        max_words (int): Maximum number of words in a sentence.

    Returns:
        int: Index of the last word of the sentence that contains the word at word_index.
    """

    def is_word_sentence_end(x):
        return x >= 0 and word_list[x][-1] in sentence_ending_punctuations

    right_idx = word_idx
    while (
        right_idx < len(word_list)
        and right_idx - word_idx < max_words
        and not is_word_sentence_end(right_idx)
    ):
        right_idx += 1

    return (
        right_idx
        if right_idx == len(word_list) - 1 or is_word_sentence_end(right_idx)
        else -1
    )


def get_realigned_ws_mapping_with_punctuation(
    word_speaker_mapping, max_words_in_sentence=50
):
    """This function realigns the speaker labels in the word_speaker_mapping based on the punctuation marks.

    Args:
        word_speaker_mapping (list): List of dictionaries containing the word, speaker, start_time, and end_time.
        max_words_in_sentence (int): Maximum number of words in a sentence. Default is 50.

    Returns:
        list: List of dictionaries containing the word, speaker, start_time, and end_time.
    """

    def is_word_sentence_end(x):
        return (
            x >= 0
            and word_speaker_mapping[x]["word"][-1] in sentence_ending_punctuations
        )

    wsp_len = len(word_speaker_mapping)

    words_list, speaker_list = [], []
    for k, line_dict in enumerate(word_speaker_mapping):
        word, speaker = line_dict["word"], line_dict["speaker"]
        words_list.append(word)
        speaker_list.append(speaker)

    k = 0
    while k < len(word_speaker_mapping):
        line_dict = word_speaker_mapping[k]
        if (
            k < wsp_len - 1
            and speaker_list[k] != speaker_list[k + 1]
            and not is_word_sentence_end(k)
        ):
            left_idx = get_first_word_idx_of_sentence(
                k, words_list, speaker_list, max_words_in_sentence
            )
            right_idx = (
                get_last_word_idx_of_sentence(
                    k, words_list, max_words_in_sentence - k + left_idx - 1
                )
                if left_idx > -1
                else -1
            )
            if min(left_idx, right_idx) == -1:
                k += 1
                continue

            spk_labels = speaker_list[left_idx : right_idx + 1]
            mod_speaker = max(set(spk_labels), key=spk_labels.count)
            if spk_labels.count(mod_speaker) < len(spk_labels) // 2:
                k += 1
                continue

            speaker_list[left_idx : right_idx + 1] = [mod_speaker] * (
                right_idx - left_idx + 1
            )
            k = right_idx

        k += 1

    k, realigned_list = 0, []
    while k < len(word_speaker_mapping):
        line_dict = word_speaker_mapping[k].copy()
        line_dict["speaker"] = speaker_list[k]
        realigned_list.append(line_dict)
        k += 1

    return realigned_list


def initialize_sentence(speaker, start_time, end_time):
    speaker_name = "Main Speaker" if speaker == 0 else f"Speaker {speaker}"
    return {
        "speaker": speaker_name,
        "start_time": start_time,
        "end_time": end_time,
        "text": "",
    }


def get_sentences_speaker_mapping(word_speaker_mapping, speaker_timestamps):
    """Get the sentences with their respective speakers.

    Args:
        word_speaker_mapping (list): List of dictionaries containing the word, speaker, start_time, and end_time.
        speaker_timestamps (list): List of tuples containing the start_time, end_time, and speaker.

    Returns:
        list: List of dictionaries containing the speaker, start_time, end_time, and text.
    """

    sentence_checker = nltk.tokenize.PunktSentenceTokenizer().text_contains_sentbreak
    start, end, speaker = speaker_timestamps[0]
    prev_speaker = speaker

    snts = []

    snt = initialize_sentence(speaker, start, end)

    # if speaker is 0, then it's the main speaker
    if speaker == 0:
        snt["speaker"] = "Main Speaker"

    for wrd_dict in word_speaker_mapping:
        wrd, speaker = wrd_dict["word"], wrd_dict["speaker"]
        start, end = wrd_dict["start_time"], wrd_dict["end_time"]
        if speaker != prev_speaker or sentence_checker(snt["text"] + " " + wrd):
            snts.append(snt)
            snt = initialize_sentence(speaker, start, end)

        else:
            snt["end_time"] = end

        snt["text"] += wrd + " "
        prev_speaker = speaker

    snts.append(snt)

    # if 1st sentence has speaker 0, then it's the main speaker
    if snts[0]["speaker"] == "Speaker 0":
        snts[0]["speaker"] = "Main Speaker"
    return snts


def replace_speaker_0_with_main_speaker(sentences_speaker_mapping):
    """Replace 'Speaker 0' with 'Main Speaker' in the sentences."""
    for sentence_dict in sentences_speaker_mapping:
        if sentence_dict["speaker"] == "Speaker 0":
            sentence_dict["speaker"] = "Main Speaker"

    return sentences_speaker_mapping


def get_speaker_aware_transcript(sentences_speaker_mapping, f):
    previous_speaker = sentences_speaker_mapping[0]["speaker"]
    f.write(f"{previous_speaker}: ")

    for sentence_dict in sentences_speaker_mapping:
        speaker = sentence_dict["speaker"]
        sentence = sentence_dict["text"]

        # If this speaker doesn't match the previous one, start a new paragraph
        if speaker != previous_speaker:
            f.write(f"\n\n{speaker}: ")
            previous_speaker = speaker

        # No matter what, write the current sentence
        f.write(sentence + " ")


def format_timestamp(
    milliseconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert milliseconds >= 0, "non-negative timestamp expected"

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


def write_srt(transcript, file):
    """
    Write a transcript to a file in SRT format. (unused as of now)

    """
    for i, segment in enumerate(transcript, start=1):
        # write srt lines
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start_time'], always_include_hours=True, decimal_marker=',')} --> "
            f"{format_timestamp(segment['end_time'], always_include_hours=True, decimal_marker=',')}\n"
            f"{segment['speaker']}: {segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )


def find_numeral_symbol_tokens(tokenizer):
    numeral_symbol_tokens = [
        -1,
    ]
    for token, token_id in tokenizer.get_vocab().items():
        has_numeral_symbol = any(c in "0123456789%$£" for c in token)
        if has_numeral_symbol:
            numeral_symbol_tokens.append(token_id)
    return numeral_symbol_tokens


def _get_next_start_timestamp(word_timestamps, current_word_index, final_timestamp):
    # if current word is the last word
    if current_word_index == len(word_timestamps) - 1:
        return word_timestamps[current_word_index]["start"]

    next_word_index = current_word_index + 1
    while current_word_index < len(word_timestamps) - 1:
        if word_timestamps[next_word_index].get("start") is None:
            # if next word doesn't have a start timestamp
            # merge it with the current word and delete it
            word_timestamps[current_word_index]["word"] += (
                " " + word_timestamps[next_word_index]["word"]
            )

            word_timestamps[next_word_index]["word"] = None
            next_word_index += 1
            if next_word_index == len(word_timestamps):
                return final_timestamp

        else:
            return word_timestamps[next_word_index]["start"]


def filter_missing_timestamps(
    word_timestamps, initial_timestamp=0, final_timestamp=None
):
    # handle the first and last word
    if word_timestamps[0].get("start") is None:
        word_timestamps[0]["start"] = (
            initial_timestamp if initial_timestamp is not None else 0
        )
        word_timestamps[0]["end"] = _get_next_start_timestamp(
            word_timestamps, 0, final_timestamp
        )

    result = [
        word_timestamps[0],
    ]

    for i, ws in enumerate(word_timestamps[1:], start=1):
        # if ws doesn't have a start and end
        # use the previous end as start and next start as end
        if ws.get("start") is None and ws.get("word") is not None:
            ws["start"] = word_timestamps[i - 1]["end"]
            ws["end"] = _get_next_start_timestamp(word_timestamps, i, final_timestamp)

        if ws["word"] is not None:
            result.append(ws)
    return result


def cleanup(path: str):
    """Clean up a file or directory. Path can be either relative or absolute."""
    # check if file or directory exists
    if os.path.isfile(path) or os.path.islink(path):
        # remove file
        os.remove(path)
    elif os.path.isdir(path):
        # remove directory and all its content
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))


def process_language_arg(language: str, model_name: str):
    """
    Process the language argument to make sure it's valid and convert language names to language codes.
    """
    if language is not None:
        language = language.lower()
    if language not in LANGUAGES:
        if language in TO_LANGUAGE_CODE:
            language = TO_LANGUAGE_CODE[language]
        else:
            raise ValueError(f"Unsupported language: {language}")

    if model_name.endswith(".en") and language != "en":
        if language is not None:
            logging.warning(
                f"{model_name} is an English-only model but received '{language}'; using English instead."
            )
        language = "en"
    return language
