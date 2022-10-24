# pip-resolved

## Why?
With tools such as Poetry, PDM and pip-tools and we can now build wheels with pinned dependencies, resolved at development time. Unfortunately, pip doesn't offer an easy way to install that without performing a full dependency-tree resolution at install time, which slows down the process.

**pip-resolved** was created as a thin wrapper around pip's existing functionality to allow users to install wheels with pre-resolved dependencies, without the need to package an extra requirements.txt or contraints file.

This is specially useful for **applications** (not libraries) that are being distributed as wheels with a fixed set of pinned dependencies to ensure reproducibility.

## Installation

### With pip
```shell
$ pip install pip-resolved
```

### With pipx
```shell
$ pipx install pip-resolved
```

## Usage
As simple as :point_down:
```shell
$ pip-resolved install <WHEEL>
```


## How it works
**pip-resolved** extracts all pinned dependencies defined as `Requires-Dist` on your artifact metadata, generates a temporary requirements.txt file and executes the following command

```shell
$ pip install --no-deps -r requirements.txt <WHEEL>
```

The `--no-deps` command is key to make sure pip doesn't attempt to resolve the whole dependency tree.
