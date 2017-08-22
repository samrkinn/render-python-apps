import os
import json
from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Bool, Float, Int, Nested, Str, List
from argschema.schemas import DefaultSchema
import renderapi
from ..module.render_module import RenderModule, RenderParameters

class TransformParameters(DefaultSchema):
	type = Str(required=True,
		description='')
	className = Str(required=True,
		description='')
	dataString = Str(required=True,
		description='')

class ApplyLensCorrectionParameters(RenderParameters):
	inputStack = Str(required=True,
		description='')
	outputStack = Str(required=True,
		description='')
	zs = List(Int, required=True,
		description='')
	transform = Nested(TransformParameters)
	refId = Str(allow_none=True, required=True,
		description='')

class ApplyLensCorrection(RenderModule):
	def __init__(self, *args, **kwargs):
		super(ApplyLensCorrection, self).__init__(schema_type = 
			ApplyLensCorrectionParameters, *args, **kwargs)

	def run(self):
		render = self.args['render']
		inputStack = self.args['inputStack']
		outputStack = self.args['outputStack']
		zs = self.args['zs']
		transform = self.args['transform']
		refId = self.args['refId']

		# output dict
		output = {
			"stack": "",
			"refId": ""
		}

		r = self.render

		# new tile specs for each z selected
		new_tspecs = []
		for z in zs:
			tspecs = renderapi.tilespec.get_tile_specs_from_z(inputStack, z, 
				render=r)

			for ts in tspecs:
				lc_tform = renderapi.transform.Transform(json=transform)
				ts.tforms = [lc_tform] + ts.tforms
				new_tspecs.append(ts)

		# statement to delete stack if desired
		# renderapi.stack.delete_stack(outputStack, render=r)

		# """
		renderapi.stack.create_stack(outputStack, render=r)
		renderapi.stack.set_stack_state(outputStack, 'LOADING', render=r)
		renderapi.client.import_tilespecs(outputStack, new_tspecs, render=r)
		renderapi.stack.set_stack_state(outputStack, 'COMPLETE', render=r)
		# """

		output['stack'] = outputStack
		output['refId'] = "8ccxdfs394875asdv"

if __name__ == '__main__':
	example_input = {
		"render": {
			"host": "em-131fs",
			"port": 8080,
			"owner": "samk",
			"project": "RENDERAPI_TEST",
			"render_client_scripts": """/allen/programs/celltypes/workgroups/
				em-connectomics/russelt/render_mc.old/render-ws-java-client/
				src/main/scripts"""
		},
		"inputStack": "test_noLC",
		"outputStack": "test_LC",
		"zs": [2266],
		"transform": {
			"type": "leaf",
			"className": "lenscorrection.NonLinearTransform",
			"dataString": """5 21 1078.539787490504 5.9536401731869155 
				18.082459176969103 1078.355487979244 3.5307003058070348 
				11.64046339965791 -2.0439286697147363 -24.64074017045258 
				-41.26811513301735 -9.491349156078 -1.6954196055547417 
				-9.185363883704582 3.2959653136929163 16.063471152021727 
				16.294847510892705 11.433417367508135 31.814503296730077 
				8.568546283786144 1.1875763257283882 1.8390027135003706 
				4.811216491589896 -6.951845669522106 -12.267142955347461 
				-15.925381113080153 -14.870929614388771 -1.4936338107986824 
				-14.329785142195151 -10.312907851336057 -0.42262010802849903 
				-1.009175398784258 -3.2394612925182904 1.1172748871012366 
				3.675506795700918 4.147928095339033 4.180779006453825 
				2.3467092081149583 3.126555229782104 -0.7606672639855052 
				4.694244302355039 4.905604855794568 19.42462457061161 
				17.804784158940837 1942.4644352489915 1780.4747249033032 
				4947240.512601199 3472086.434895099 4297903.568850483 
				1.4156910200690086E10 8.869224932399399E9 8.401913335029685E9 
				1.184452643883111E10 4.326915271956289E13 
				2.5462360962795074E13 2.1493026326968934E13 
				2.3188186000529023E13 3.519602640946822E13 
				1.3795333182608984E17 7.805152532090952E16 
				6.180627842946396E16 5.937108087578708E16 
				6.8994694539978896E16 1.09803035347323568E17 100.0 
				1083.561059814147 1062.000092490804 4335259.912658479 
				3072116.6105437097 4089560.9959054096 1.588497037768282E10 
				1.054070313855633E10 1.0306317022320707E10 
				1.463025351609144E10 5.735536632714905E13 
				3.677632888097447E13 3.3248028854072227E13 
				3.53752851004701E13 5.205228949477172E13 
				2.06753448194955584E17 1.29851821487233248E17 
				1.12997804746083296E17 1.1130902498005392E17 
				1.23651446458254E17 1.85995206005396736E17 0.0 3840 3840 """
		},
		"refId": None
	}

	# remove tabs, endlines from dataString formatting above
	example_input['transform']['dataString'] = example_input['transform']['dataString'].replace('\n\t\t\t\t', '')

	module = ApplyLensCorrection(input_data = example_input)
	module.run()