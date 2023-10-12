# Team Fudan 2023 Software Tool                           

![](https://static.igem.wiki/teams/4765/wiki/czy/rap-logo.png)

![](https://badgen.net/badge/platform/Linux,macOS,Windows?list=%7C)
![](https://badgen.net/static/Python/3.10/blue)
![](https://badgen.net/static/vue/2.6+/green)
![](https://badgen.net/static/license/CC%20BY%204.0/blue)
![](https://badgen.net/docker/size/mistyfield/rap/0.4.1-beta)

RAP is a quantitative pRAP system design software developed by Fudan iGEM 2023. Live demo of RAP is available. Visit our live demo [here](http://54.169.242.254:5000/)!

## Description

For more information, please visit our [wiki page](https://2023.igem.wiki/fudan/software).

### Features

- Intuitive WebUI with APIs for flexible development
- Compatible with GenBank format, and easy integration with [SnapGene(opens new window)](https://www.snapgene.com/)
- Full DBTL cycle support
- Experimentally validated results
- Up-to-date documentation and tutorial videos

## Installation

### Supported platforms

|    Windows     |  Linux   |  macOS   |
| :------------: | :------: | :------: |
| ✅(wsl2, amd64) | ✅(amd64) | ✅(amd64) |



## Install with docker(recommended)

Since the installation process requires docker, please install [docker](https://www.docker.com/) first.

```shell
docker pull mistyfield/kinetichub:v0.1.0-beta mistyfield/rap:0.4.1-beta mistyfield/parthub:0.1.0-beta
docker run -p 3306:3306 kinetichub
docker run -p 5000:5000 rap
docker run -p 7474:7474 -p 7687:7687 parthub
```

## Install with source code

This project requires the use of docker and yarn for deployment, so please install [docker](https://www.docker.com/) and [node.js](https://nodejs.org/en) with [yarn](https://yarnpkg.com/) first!

```shell
git clone https://gitlab.igem.org/2023/software-tools/fudan
# compile webUI
cd fudan/webUI
yarn install
cd ../
sh pack.sh
docker compose up -d
```

After that RAP will be running at http://127.0.0.1:5000.

## Usage

For more information on Usage, please visit our [wiki](https://2023.igem.wiki/fudan/software/) or [documentation](https://mistyfield.github.io/RAP-Docs/).


## Contributing
### Pull Requests

We actively welcome your pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Make sure your code lints.

In order to accept your pull request, please send me an [email](mailto:20301050198@fudan.edu.cn).

### Issues

We use GitLab issues to track bugs. Please describe your issue clearly and give sufficient instructions to reproduce the issue.

## Authors and acknowledgment
### Author

- Zhiyue Chen ([@mistyfield](https://gitlab.igem.org/mistyfield))
