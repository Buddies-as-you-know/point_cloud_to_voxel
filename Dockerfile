# Use the official Ubuntu 22.04 image from the Docker Hub
FROM ubuntu:22.04

# Set the working directory inside the container
WORKDIR /app

# Set time zone
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update the system and upgrade the packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the necessary packages
RUN apt-get update \
    && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libbz2-dev \
    libnss3-dev \
    libsqlite3-dev \
    libssl-dev \
    liblzma-dev \
    libreadline-dev \
    libffi-dev \
    libgl1-mesa-dev \
    locales \
    fish \
    vim \
    iputils-ping \
    net-tools \
    software-properties-common \
    fonts-powerline

# Install fisher and set fish as the default shell
RUN chsh -s /usr/bin/fish
RUN fish -c "curl -sL https://git.io/fisher | source ; fisher install jorgebucaran/fisher"
RUN fish -c "fisher install oh-my-fish/theme-bobthefish"

# Install pyenv
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Add pyenv settings to fish config
RUN mkdir -p ~/.config/fish
RUN echo 'set -x PYENV_ROOT $HOME/.pyenv' >> ~/.config/fish/config.fish
RUN echo 'set -x PATH  $PYENV_ROOT/bin $PATH' >> ~/.config/fish/config.fish
RUN echo 'set -x PATH $PYENV_ROOT/shims $PATH' >> ~/.config/fish/config.fish
RUN echo 'status --is-interactive; and source (pyenv init -|psub)' >> ~/.config/fish/config.fish

# Add pyenv settings to bashrc
RUN echo '' >> ~/.bashrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

# Download and install Python 3.10.7
RUN fish -c "pyenv install 3.10.7"
RUN fish -c "pyenv global 3.10.7"

# Set environment variables
ENV PYENV_ROOT=/root/.pyenv
ENV PATH=$PYENV_ROOT/bin:$PATH

# Configure locale
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /app/requirements.txt
RUN fish -c  "pip install --upgrade pip"
RUN fish -c "pip install --no-cache-dir -r requirements.txt"

# This environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED True