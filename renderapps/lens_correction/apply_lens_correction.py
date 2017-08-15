import os
import json
from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Bool, Float, Int, Nested, Str, List
from argschema.schemas import DefaultSchema
import renderapi
from ..module.render_module import RenderModule, RenderParameters

class TransformParameters(DefaultSchema):
	tf_type = Str(required=True,
		description='')
	className = Str(required=True,
		description='')
	dataString = Str(required=True,
		description='')

class ApplyLensCorrectionParameters(RenderParameters):
	stack = Str(required=True,
		description='')
	zs = List(Int, required=True,
		description='')
	transform = Nested(TransformParameters)
	refId = String(allow_none=True, required=True,
		description='')

class ApplyLensCorrection(RenderModule):
	def __init__(self, *args, **kwargs):
		super(ApplyLensCorrection, self).__init__(schema_type = 
			ApplyLensCorrectionParameters, *args, **kwargs)

	def run(self):
		print self.args

		output = {
			"stack": "",
			"refId": ""
		}

		# Build stack from z(s) with lens correction

		output['stack'] = self.args['output_stack']
		output['refId'] = "8ccxdfs394875asdv"

		print 'DONE!'

if __name__ == '__main__':
	example_input = {
		"render": {
			"host": "em-131fs",
			"port": 8080,
			"owner": "renderowner",
			"project": "SPECIMEN",
			"render_client_scripts": "/PATH/TO/CLIENTSCRIPTS/"
		},
		"input_stack": "MONTAGESTACK1",
		"output_stack": "MONTAGESTACK2",
		"zs": 2201,
		"transform": {
			"tf_type": "leaf",
			"className": "lenscorrection.NonLinearTransform",
			"dataString": "5 21 1056.1583492292154 5.643427565050266 ... 1.41164653564974448E17 1.99258104942372064E17 0.0 3840 3840 "
		},
		"refId": "None"
	}

	module = ApplyLensCorrection(input_data = example_input)
	module.run()