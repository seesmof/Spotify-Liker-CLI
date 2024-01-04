<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/seesmof/">
    <img src="./public/logo.png" alt="Logo" height="80">
  </a>

<h1 align="center">Spotify Batch Liker</h1>
</div>

### Table of contents

- [Table of contents](#table-of-contents)
- [Installation Instructions](#installation-instructions)
- [Usage Tips](#usage-tips)
  - [Getting authentication credentials](#getting-authentication-credentials)
  - [Confirming authorizaiton](#confirming-authorizaiton)
- [Screenshots](#screenshots)
- [Links](#links)
- [License](#license)

### Installation Instructions

- Download [latest version](https://github.com/seesmof/spotify-playlist-liker/releases) of the app
  - Make sure you have Python 3.10 or later installed. If not, please do so - [latest version](https://www.python.org/downloads/)
- Unarchive the archive you got
- Open and run `Run.bat` file
- Enjoy!

### Usage Tips

#### Getting authentication credentials

To use this app, you will need to create a Spotify application in `Spotify for Developers`. To do that, please follow the steps below, it is not hard at all.

1. Go to the [Spotify for Developers](https://developer.spotify.com/dashboard/) website.
2. Log in with your Spotify account or sign up for a new account if you don't have one.
3. Click on the "Create an App" button.
4. Fill in the required information for your app, including the name and description.
5. After creating the app, you will be provided with a `client ID` and a `client secret`. These are unique identifiers for your app.
6. Make note of the `client ID` and `client secret` as you will need them later.
7. Set the `redirect URL` for your app. This is the URL that Spotify will redirect to after the user grants permission to your app.
8. Once you have completed these steps, you can use the `client ID`, `client secret`, and `redirect URL` in your code.

#### Confirming authorizaiton

While using the app, after selecting your playlist and the action you want to perform, a new browser page may open in your default browser and ask for your authorization. If this happens, click on the "Allow" button. After that, you will be redirected to a page that corresponds to the `redirect URL` you specified earlier. Copy the URL of that page and, when prompted with the message `Enter the URL you were redirected to`, paste it in the console and press Enter.

### Screenshots

![App](./public/app.png)

### Links

- [Icon](https://www.flaticon.com/)

### License

This project is licensed under the [MIT License](./LICENSE).

<p align="right"><a href="#readme-top"><strong>Back to top</strong></a></p>
