import renderapi
import os
from ..module.render_module import RenderModule, RenderParameters
from json_module import InputFile,InputDir
import marshmallow as mm
import json

example_parameters={
    "render":{
        "host":"ibs-forrestc-ux1",
        "port":80,
        "owner":"S3_Run1",
        "project":"S3_Run1_Jarvis",
        "client_scripts":"/pipeline/render/render-ws-java-client/src/main/scripts"
    },
    "matchcollections":['S3_Run1_Jarvis_68_to_112_DAPI_1_highres_R1'],
    "input_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-145-165-nostitch-EDIT.json",
    "output_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-145-165-nostitch-QC.json",
    "figdir":"/nas3/data/S3_Run1_Jarvis/processed/matchfigures",
    "min_matches":5
}

example_parameters={
    "render":{
        "host":"ibs-forrestc-ux1",
        "port":80,
        "owner":"S3_Run1",
        "project":"S3_Run1_Jarvis",
        "client_scripts":"/pipeline/render/render-ws-java-client/src/main/scripts"
    },
    "matchcollections":['S3_Run1_Jarvis_68_to_112_DAPI_1_highres_R1'],
    "input_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-170-200-nostitch-EDIT.json",
    "output_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-170-200-nostitch-QC.json",
    "figdir":"/nas3/data/S3_Run1_Jarvis/processed/matchfigures",
    "min_matches":5
}
#example_parameters={
#    "render":{
#        "host":"ibs-forrestc-ux1",
#        "port":80,
#        "owner":"S3_Run1",
#        "project":"S3_Run1_Jarvis",
#        "client_scripts":"/pipeline/render/render-ws-java-client/src/main/scripts"
#    },
#    "matchcollections":['S3_Run1_Jarvis_68_to_112_DAPI_1_highres_R1'],
#    "input_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-300-400-nostitch-EDIT.json",
#    "output_tilepairfile":"/nas4/data/S3_Run1_Jarvis/processed/tilepairfiles1/tilepairs-10-300-400-nostitch-QC.json",
#    "figdir":"/nas3/data/S3_Run1_Jarvis/processed/matchfigures",
#    "min_matches":5
#}
class QCPointMatchResultsParameters(RenderParameters):
    matchcollections = mm.fields.List(mm.fields.Str,required=True,
        metadata={'description':'list of match collections to analyze'})
    input_tilepairfile = InputFile(required=True, 
        metadata = {'description':'file path of tile pair file to qc'})
    output_tilepairfile = mm.fields.Str(required=True,
        metadata = {'description':'file path of where to save the tile pair file to qc'})
    figdir = mm.fields.Str(required=True,
        metadata={'description':'directory to save images'})
    min_matches = mm.fields.Int(required=False,default=5,
        metadata={'description':'number of matches between tiles to be considered a valid match'})
    pool_size = mm.fields.Int(required=False,default=20,
        metadata={'description':'number of parallel threads to use'})

    
class QCPointMatchResults(RenderModule):
    def __init__(self,schema_type=None,*args,**kwargs):
        if schema_type is None:
            schema_type = QCPointMatchResultsParameters
        super(QCPointMatchResults,self).__init__(schema_type=schema_type,*args,**kwargs)

    def run(self):
        with open(self.args['input_tilepairfile'],'r') as fp:
            tilepairjson = json.load(fp)
    
        bad_tilepairjson,match_numbers = get_bad_pairs(self.render,
            tilepairjson,
            self.args['matchcollections'],
            self.args['min_matches'],
            self.args['pool_size'])

        define_connected_components_by_section(self.render,
            tilepairjson,
            match_numbers,
            pool_size = self.args['pool_size'])

        with open(self.args['output_tilepairfile'],'w') as fp:
            json.dump(bad_tilepairjson,fp)

        #figdir='%s-%s-%s'%(self.args['figdir'],self.args['matchcollection'],stack)
        #if not os.path.isdir(figdir):
        #     os.makedirs(figdir)

 
        
if __name__ == "__main__":
    mod = QCPointMatchResults(input_data = example_parameters)
    mod.run()

