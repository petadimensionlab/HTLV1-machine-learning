# Use the official Jupyter base image
FROM jupyter/base-notebook:latest

# Set the working directory in the container
WORKDIR /home/jovyan/work

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Jupyter Notebook into the container
COPY HTLV_final.ipynb .

# Expose the default Jupyter port
EXPOSE 8888

# Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]









