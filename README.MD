# Azn Dumpster Repo ~ for personal use in adding to Kodi 19
This repo initially to host icdrama plugin updates since Azndhusband has gone dark; lately this repo to host other plugins that are not accessible directly from Kodi.

## Source Code
### Azndhusband ~ ICDRAMA source
Intial owner was https://github.com/aznhusband/aznhusband.github.io but since Nov 2020 he has gone dark.
#### ICDRAMA Files
```
  |- /src/plugin.video.icdrama/*
  |- /src/createRelease.sh
  |- /src/kodidirlist.py
  |- /src/mkdist.sh
  |- /src/mkmd5sum.sh
```

### Soraxas ~ ICDRAMA source
Voluntarily taken over by Soraxas (with other contributors) with latest updates https://github.com/soraxas/aznhusband.github.io/releases 

Going forward matching to Soraxas release version starting with 2.3.1

### Gujal00 Resolverurl
see https://github.com/Gujal00/ResolveURL and https://github.com/Gujal00/smrzips


### Kodi Repo Installation
See https://azndoodle.github.io/kodi_repo/repo/

### Build Code specific for ICDRAMA
navigate to `/src` folder and run script using one of the following:
```sh
./createRelease.sh
sh createRelease.sh
bash createRelease.sh
```
see below in description of supporting scripts

### Script Breakdown
#### ```./src/createRelease.py``` (python2 script)
Generate the artefacts needed for plugin for Kodi and uses the below scripts to support the process.

#### ```./src/kodidirlist.py``` (python2 script)
To generate html index content listing for your repo, navigate to `repo` folder and run below command.
In Windows (CMD) or MAC (Terminal) navigate to the repo folder and type: `python3 ../src/kodidirlist.py > index.html`
(You will want to run this on it's own after running the `_repo_xml_generator_v2.py`)

#### ```./src/mkmd5sum.sh```  (shell script)
To generate md5 checksum on addons.xml needed for Kodi (to run separately if this md5 needs updating manually ~ generator auto creates one)
In Windows (CMD) or MAC (Terminal) navigate to the src folder and type: `python3 mkmd5sum.sh`

#### ```./src/mkdist.sh``` (shell script)
(??) Not sure what is the need or what it's suppose to do.


# Changelog
### 2023-01-02
- bump repo version to 1.1.0
- add Gujal00 resolverurl repo to the list
- update `index.html` with instructions
- updated to 2.3.2 from icdrama `/src` from Soraxas release

### prior in 2022
- creating this repo and bring in previous icdrama 2.2.0



---
# Tutorial of Kodi Repo and Plugin Project
Video version of this tutorial now available!
[How to make a Kodi Repository!](https://youtu.be/EgFtVW0MRrs)

this readme has been modified for better organization of code and may not match the video link.

## CHANGES - definition and minor changes to the original

### Original Tutorial Files
```
  |- /repo/index.html 
  |- /src/repository.example
  |- /_repo_xml_generator.py
  |- /README.MD
```

### Folder Structure
`src` folder - stores all source codes needed to generate the final artifact (zips)
`zip` folder - (generated) stores the newly generated artifacts from the src folder (once repo is installed, this is where it will fetch the plugins)
`repo` folder - (generated) stores repositories to your zips and other additinal repo you want to make available (Kodi will look here in file manager for repo/zips to install)



## BASIC - How to setup for hosting on GitHub Pages

In order to follow this tutorial, first fork this repository, and then clone your newly forked copy locally.

First, you'll need to edit the `addon.xml` file within the `/src/repository.example` folder with your chosen add-on ID, a version number, and your username (or whatever you'd like) for `provider`, as seen on line 2:

```XML
<addon id="ADDON_ID_HERE" name="REPO_NAME_HERE" version="VERSION_NUMBER_HERE" provider-name="YOUR_USERNAME_HERE">
```

You also need to replace `YOUR_USERNAME_HERE` and `REPOSITORY_NAME_HERE` with your GitHub username and this repository's name, respectively, as seen on lines 5-7:

```XML
<info compressed="false">https://raw.githubusercontent.com/YOUR_USERNAME_HERE/REPOSITORY_NAME_HERE/master/zips/addons.xml</info>
<checksum>https://raw.githubusercontent.com/YOUR_USERNAME_HERE/REPOSITORY_NAME_HERE/master/zips/addons.xml.md5</checksum>
<datadir zip="true">https://raw.githubusercontent.com/YOUR_USERNAME_HERE/REPOSITORY_NAME_HERE/master/zips/</datadir>
```

You should also change the summary and description of your repository, as seen on lines 11-12:

```XML
<summary>REPO_NAME_HERE</summary>
<description>DESCRIPTION OF YOUR REPO HERE</description>
```

While not required, it is also recommended to replace `icon.png` and `fanart.jpg` in the `/repository.example` folder with art relevant to your repository or the add-ons contained within. `icon.png` should be 512x512 px, and `fanart.jpg` should be 1920x1080 px, or a similar ratio.

To build the repository, first rename the `/repository.example` folder to match whatever add-on ID you chose earlier. Place the add-on source folders for whichever add-ons you'd like to be contained in your Kodi repo in the main folder of this repository, and run `_repo_xml_generator.py`. 

In Windows (CMD) or MAC (Terminal) type: `python3 _repo_xml_generator.py`

UPDATE 1: moved `/repository.example` to `/src/repository.example`.
UPDATE 2: type, `python3 _repo_xml_generator_v2.py` ~ fixed generated zip as it was generating zero size zips.


This will create zips of all of the desired add-ons, and place them in the `zips` folder, along with a generated `addons.xml` and `addons.xml.md5`. Copy the zip file of your repository, located at `/zips/ADDON_ID_HERE/ADDON_ID_HERE-VERSION_NUMBER_HERE.zip`,
and paste it into the `/repo` folder.

Inside the `/repo` folder, edit the link inside `index.html` to reflect your add-on's filename, as seen on line 1:

```HTML
<a href="ADDON_ID_HERE-VERSION_NUMBER_HERE.zip">ADDON_ID_HERE-VERSION_NUMBER_HERE.zip</a>
```

After committing and pushing these changes to your repo, go to the "Settings" section for this repository on GitHub. In the first box, labeled "Repository name", change your repository's name. Generally, GitHub Pages repositories are named `YOUR_USERNAME_HERE.github.io`,  but it can be whatever you'd like.
Next, scroll down to the "GitHub Pages" section, choose the `master` branch as the source, and click "Save".

After that, you should be all done!

If you named this repository `YOUR_USERNAME_HERE.github.io`, your file manager source will be:

`https://YOUR_USERNAME_HERE.github.io/repo/`

And if you named it something else, it will be:

`https://YOUR_USERNAME_HERE.github.io/REPOSITORY_NAME_HERE/repo/`

## ADVANCED - How to set up for hosting without GitHub Pages

If you want to host your Kodi repo on a different host besides GitHub Pages, simply download this repository as a `.zip`, and unzip it , rather than forking and cloning it. Continue to follow the rest of the setup procedure, except for the setting up of GitHub Pages. The only differences will be in your `addon.xml` file (lines 5-7), as it will need to reference yourhost, rather than GitHub:

```XML
<info compressed="false">https://YOUR_HOST_URL_HERE/zips/addons.xml</info>
<checksum>https://YOUR_HOST_URL_HERE/zips/addons.xml.md5</checksum>
<datadir zip="true">https://YOUR_HOST_URL_HERE/zips/</datadir>
```

And upload the contents of this repository to your host. It is **very important** that `YOUR_HOST_URL_HERE` is the URL to *this* folder.

After doing so, your file manager source will be:

`https://YOUR_HOST_URL_HERE/repo/`

## WHAT'S IMPORTANT TO KODI
- ***addons.xml.md5***: contains the checksum to addons.xml.  This value is stored in Kodi database. If the MD5 remains the same, Kodi won't query the addons.xml.
- ***addons.xml***: used by Kodi to infer the contents of the repo or addon.





