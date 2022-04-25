# eniarof-pillard-tangram
This is an attraction built for ENIAROF#32 at the format Pillard factory in Marseille.

## Technology
This is attraction runs on the following hardware/software/objects
- [Luxonis OAK-1]()
- [Raspberry Pi 4]()
- A light table
- Tanram pieces
- Amplified Speakers

## Annotation
We have to annotate our images. For now, we're using Roboflow, with the following project id: [eniarof-pillard-tangram](https://app.roboflow.com/eniarof/eniarof-pillard-tangram/).

## Training
We are using

## Conda (Mac)

```
$ conda activate DepthAIEnv39
```

To activate Conda, I used the `conda activate DepthAIEnv39` command. I guess (I assume) this loaded all the relevant DepthAI into that Python environment inside conda. I guess. I still don't really understand how Conda works. You should see this:

```
(DepthAIEnv39) abstractmachine@abstract-maxbook depthai-python %
```

If you wish to return to `(base)` anaconda:

```
$ conda activate
```

To turn off anaconda:

```
$ conda deactivate
```

To turn off auto-activation (very annoying):

```
$ conda config --set auto_activate_base false