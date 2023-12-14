FROM andreysenov/firebase-tools
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF
LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.name="firebase-tools" \
      org.label-schema.version=${VERSION} \
      org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.description="Firebase CLI on the NodeJS image" \
      org.label-schema.url="https://github.com/firebase/firebase-tools/" \
      org.label-schema.vcs-url="https://github.com/AndreySenov/firebase-tools-docker/" \
      org.label-schema.vcs-ref=${VCS_REF}
ENV FIREBASE_TOOLS_VERSION=${VERSION}
ENV HOME=/home/node
COPY test-requirements.txt .
USER root
RUN apt update -y && \
    apt install -y python3-pip
USER node
RUN pip3 install --break-system-packages --no-cache-dir -r test-requirements.txt

WORKDIR /home/node
COPY firebase.json .
COPY flask_firebaseauth.py .
COPY test_firebaseauth.py .
CMD ["firebase", "emulators:exec", "--project",  "test", "python3 -m unittest test_firebaseauth"]
