import os
import json
import subprocess
from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Bool, Float, Int, Nested, Str
from argschema.schemas import DefaultSchema
import renderapi

class SIFTParameters(DefaultSchema):
    initialSigma = Float(required=True,
        description='')
    steps = Int(required=True,
        description='')
    minOctaveSize = Int(required=True,
        description='')
    maxOctaveSize = Int(required=True,
        description='')
    fdSize = Int(required=True,
        description='')
    fdBins = Int(required=True,
        description='')

class AlignmentParameters(DefaultSchema):
    rod = Float(required=True,
        description='')
    maxEpsilon = Float(required=True,
        description='')
    minInlierRatio = Float(required=True,
        description='')
    minNumInliers = Int(required=True,
        description='')
    expectedModelIndex = Int(required=True,
        description='')
    multipleHypotheses = Bool(required=True,
        description='')
    rejectIdentity = Bool(required=True,
        description='')
    identityTolerance = Float(required=True,
        description='')
    tilesAreInPlace = Bool(required=True,
        description='')
    desiredModelIndex = Int(required=True,
        description='')
    regularize = Bool(required=True,
        description='')
    maxIterationsOptimize = Int(required=True,
        description='')
    maxPlateauWidthOptimize = Int(required=True,
        description='')
    dimension = Int(required=True,
        description='')
    lambdaVal = Float(required=True,
        description='')
    clearTransform = Bool(required=True,
        description='')
    visualize = Bool(required=True,
        description='')

class LensCorrectionParameters(ArgSchema):
    manifest_path = Str(required=True,
        description='path to manifest file')
    project_path = Str(required=True,
        description='path to project directory')
    fiji_path = Str(required=True,
        description='path to FIJI')
    grid_size = Int(required=True,
        description='')
    SIFT_params = Nested(SIFTParameters)
    align_params = Nested(AlignmentParameters)

class LensCorrectionModule(ArgSchemaParser):
    def __init__(self, *args, **kwargs):
        super(LensCorrectionModule, self).__init__(schema_type = 
            LensCorrectionParameters, *args, **kwargs)

    def run(self):
        bsh_call = ["xvfb-run",
            "-a",
            self.args['fiji_path'],
            "-Xms20g", "-Xmx20g", "-Xincgc",
            "-Dman=" + self.args['manifest_path'],
            "-Ddir=" + self.args['project_path'],
            "-Dgrid=" + str(self.args['grid_size']),
            "-Disig=" + str(self.args['SIFT_params']['initialSigma']),
            "-Dsteps=" + str(self.args['SIFT_params']['steps']),
            "-Dminos=" + str(self.args['SIFT_params']['minOctaveSize']),
            "-Dmaxos=" + str(self.args['SIFT_params']['maxOctaveSize']),
            "-Dfdsize=" + str(self.args['SIFT_params']['fdSize']),
            "-Dfdbins=" + str(self.args['SIFT_params']['fdBins']),
            "-Drod=" + str(self.args['align_params']['rod']),
            "-Dmaxe=" + str(self.args['align_params']['maxEpsilon']),
            "-Dmir=" + str(self.args['align_params']['minInlierRatio']),
            "-Dmni=" + str(self.args['align_params']['minNumInliers']),
            "-Demi=" + str(self.args['align_params']['expectedModelIndex']),
            "-Dmh=" + str(self.args['align_params']['multipleHypotheses']),
            "-Dri=" + str(self.args['align_params']['rejectIdentity']),
            "-Dit=" + str(self.args['align_params']['identityTolerance']),
            "-Dtaip=" + str(self.args['align_params']['tilesAreInPlace']),
            "-Ddmi=" + str(self.args['align_params']['desiredModelIndex']),
            "-Dreg=" + str(self.args['align_params']['regularize']),
            "-Dmio=" + 
                str(self.args['align_params']['maxIterationsOptimize']),
            "-Dmpwo=" + 
                str(self.args['align_params']['maxPlateauWidthOptimize']),
            "-Ddim=" + str(self.args['align_params']['dimension']),
            "-Dlam=" + str(self.args['align_params']['lambdaVal']),
            "-Dctrans=" + str(self.args['align_params']['clearTransform']),
            "-Dvis=" + str(self.args['align_params']['visualize']),
            "--", "--no-splash",
            "run_lens_correction.bsh"]

        subprocess.call(bsh_call)
        
if __name__ == '__main__':
    with open("input_lens_correction.json", "r") as json_file:
        example_input = json.load(json_file)

    module = LensCorrectionModule(input_data = example_input)
    module.run()