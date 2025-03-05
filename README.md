# All codes and materials

1. Install Docker:
	•	Download and install Docker Desktop from the official website.

2. Go to the "HTLV_1" repository.

3. Pull and Run the Docker Image:
	•	Open the terminal and execute:

`docker pull mdishtiakrashid/htlv_analysis_image`
`docker run -p 8888:8888 mdishtiakrashid/htlv_analysis_image`


	•	After running the container, note the URL with the token provided in the terminal output. Open this URL in a web browser to access the Jupyter notebook. From the panel bar on the left access the file.

 ## Source code for Figure 4, Supplementary Figure S6 S7

This code is most aimed for docker use (the code was only checked for Docker version 24.0.6 and 27.3.1).

Then, run the code below.

`docker image build --rm=true -t htlv1_analysis_fig4figs6figs7:latest .`

When the docker image is successfully made, run the code below and run&start the container.

`docker run --rm=true -p 8888:8888 -v $PWD:/tmp -it htlv1_analysis_fig4figs6figs7 /bin/bash`

Finally, start jupyter notebook (code_Fig4_S6_S7.ipynb) and execute the cells.

`jupyter notebook --port 8888 --ip=0.0.0.0 --allow-root --NotebookApp.token='' --notebook-dir 'tmp'`

Open the link "localhost:8888".

> **Warning**
> If another jupyter notebook is already open, the link may not open successfully.
