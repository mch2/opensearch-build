# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# About: This docker file generates an image that can be used as standard build enviornment for building all artifacts
# Usage: docker build -f standard-build.dockerfile --tag <name>
# Build arguments:
#        UID: Optional. Specify the opensearch userid. Defaults to 1000.
#        GID: Optional. Specify the opensearch groupid. Defaults to 1000.

FROM public.ecr.aws/ubuntu/ubuntu:20.04

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y git curl zip unzip iproute2

ARG UID=1000
ARG GID=1000

# Create user and group
RUN groupadd -g $GID opensearch && \
    useradd -u $UID -g $GID -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R $UID:$GID /usr/share/opensearch

COPY check.sh /usr/share/opensearch
RUN chmod +x /usr/share/opensearch/check.sh

# Java 14 is currently required for bwc tests
RUN curl -L https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U-jdk_x64_linux_hotspot_14.0.2_12.tar.gz -o jdk-14.tar.gz && \
    tar xvf jdk-14.tar.gz
ENV JAVA14_HOME="/jdk-14.0.2+12"
ENV JAVA8_HOME=/usr/lib/jvm/java-8-openjdk-amd64

USER $UID

WORKDIR /usr/share/opensearch
