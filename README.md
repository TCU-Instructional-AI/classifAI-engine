<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/TCU-Instructional-AI/classifAI-engine">
    <img src="docs/assets/logo.jpg" alt="Logo" width="128" height="128">
  </a>

<h2 align="center">ClassifAI Engine</h2>

  <p align="center">
    ClassifAI engine is a RESTful API that provides the heavy lifting for <a href="https://github.com/TCU-Instructional-AI/classifAI">classifAI</a> through audio transcription, question categorization, and insights.<br>
    <br />
    <a href="https://tcu-instructional-ai.github.io/classifAI-engine/"><strong>Explore the docs »</strong></a>
    <br /> 
    <br />
    <a href="https://github.com/TCU-Instructional-AI/classifAI">Visit Portal</a>
    ·
    <a href="https://github.com/TCU-Instructional-AI/classifAI-engine/issues">Report Bug</a>
    ·
    <a href="https://github.com/TCU-Instructional-AI/classifAI-engine/issues">Request Feature</a>
    ·
    <a href="https://github.com/TCU-Instructional-AI/classifAI/">Project Information</a>
    
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

ClassifAI engine provides the heavy lifting for classifAI. It is a RESTful API that provides the following services:

* Transcription of video and audio into text
* Categorization of questions
* Engagement insights
* Turning reports into PDFs or .docx files





### Built With

* Flask
* Celery 
* Redis
* Firebase (Storage, Firestore, Authentication)
  


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up this API locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* Python 3.8



### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/TCU-Instructional-AI/classifAI-engine.git
   ```
3. Install Python packages
   ```sh
    pip install -r requirements.txt -r requirements-dev.txt
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_




<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/TCU-Instructional-AI/classifAI/issues) for a full list of proposed features (and known issues).




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

[Learn About the Team](http://riogrande.cs.tcu.edu/2324InstructionalEffectiveness)

Project Link: [https://github.com/TCU-Instructional-AI/classifAI](https://github.com/TCU-Instructional-AI/classifAI)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TCU-Instructional-AI/classifAI.svg?style=for-the-badge
[contributors-url]: https://github.com/TCU-Instructional-AI/classifAI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TCU-Instructional-AI/classifAI.svg?style=for-the-badge
[forks-url]: https://github.com/TCU-Instructional-AI/classifAI/network/members
[stars-shield]: https://img.shields.io/github/stars/TCU-Instructional-AI/classifAI.svg?style=for-the-badge
[stars-url]: https://github.com/TCU-Instructional-AI/classifAI/stargazers
[issues-shield]: https://img.shields.io/github/issues/TCU-Instructional-AI/classifAI.svg?style=for-the-badge
[issues-url]: https://github.com/TCU-Instructional-AI/classifAI/issues
[license-shield]: https://img.shields.io/github/license/TCU-Instructional-AI/classifAI.svg?style=for-the-badge
[license-url]: https://github.com/TCU-Instructional-AI/classifAI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
