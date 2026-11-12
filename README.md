# luna lua studio

standalone lua script editor and runner. this does not inject into roblox.

## build without installing python

1. create a public github repository with the default `main` branch.
2. upload `app.py`, `README.md`, and `.github/workflows/build.yml` preserving the folder path. github's web uploader may not preserve hidden folders from some systems; if so, create `.github/workflows/build.yml` using **add file > create new file** and paste the workflow from this archive.
3. open **actions > build windows exe > run workflow** (or wait for the automatic push build).
4. when it finishes, open the run and download the `LunaLuaStudio-windows-exe` artifact zip. extract to get the exe.

only run trusted lua scripts. this runner is not a security sandbox.
