FROM node:16-alpine
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
RUN apk --no-cache add python3 py3-pip bash && \
    python -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r test-requirements.txt && \
    rm test-requirements.txt && \
    yarn global add firebase-tools@${VERSION} && \
    yarn cache clean && \
    firebase setup:emulators:database && \
    firebase setup:emulators:firestore && \
    firebase setup:emulators:pubsub && \
    firebase setup:emulators:storage && \
    firebase -V && \
    chown -R node:node $HOME

USER node
WORKDIR $HOME
COPY firebase.json .
COPY flask_firebaseauth.py .
COPY test_firebaseauth.py .
CMD ["firebase", "emulators:exec", "--project",  "test", "python -m unittest test_firebaseauth"]
