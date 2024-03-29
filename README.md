# mono

A monorepo for personal projects, experiments, and more.

## Projects

1. [GPTSmartFunc](./python/gptsmartfunc): A Proof-of-Concept project that illustrates a method for wrapping existing Python functions to generate metadata for OpenAI GPT Functions automatically. Simplifies usage and enhances maintainability.
1. [XSGPT](https://github.com/Jakob-98/xsgpt): GPT CLI with persistence in 10 lines of code and GPT RAG pattern with wikipedia in ~30 lines of code (moved to external repo). 
1. [Generate technical questions from PDF](./python/LLM_and_prompts/technical_qa_generator_from_pdf.py): Example of generating relevant QA pairs from technical documentation. Useful for various RAG scenarios and evaluation, in particular for evaluating retrieval.

## Experiments

1. [GZIP MNIST](./python/gzip_mnist/mnist_gzip.ipynb): "Solving" MNIST classification with GZIP in a few lines of code.
1. [Personal personal GPT assistant](./python/search_project/): A personal GPT assistant/boilerplate for own use.
1. [serverless-comments](./azure/serverless-comments/): Experimenting with hosting simple comments for static websites using azure functions.

## MISC

1. [Bulk git projects archiver](./python/archiving/): This script searches for Git repositories in a specified directory and its subdirectories, and creates an archive of each repository found. It bypasses the safety checks by setting up a custom Git configuration.