---
hide:
  - navigation
---

# Installation

!!! info "🔧 For client"

    The client does not need to install any program, please 
    visit [http://54.169.242.254:5000](http://54.169.242.254:5000/buildReactions)!

## Supported platforms

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