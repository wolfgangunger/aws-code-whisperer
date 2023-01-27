#!/usr/bin/env python3

import aws_cdk as cdk

from aws_code_whisperer.aws_code_whisperer_stack import AwsCodeWhispererStack


app = cdk.App()
AwsCodeWhispererStack(app, "aws-code-whisperer")

app.synth()
