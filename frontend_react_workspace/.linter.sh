#!/bin/bash
cd /home/kavia/workspace/code-generation/anonsupport-28184-8bd29d52/frontend_react_workspace/frontend_react
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

