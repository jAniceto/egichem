import pandas as pd
import numpy as np
import joblib
import argparse
import os
import sys


# Configuration variables
PIPELINE_32_PATH = 'calculators/static/calculators/ml-models/ml-gb-polar-model-32.mod'
PIPELINE_64_PATH = 'calculators/static/calculators/ml-models/ml-gb-polar-model-64.mod'
MODEL_VARIABLES = ['T', 'viscosity', 'solute.M2', 'solute.Pc', 'solvent.M1', 'solvent.elj']
OUTPUT_FILE_PATH = 'output.csv'

def get_full_path(ending):
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_file_path, ending)


def load_pipeline():
    """Load pipeline (includes scaler and model)"""
    if sys.maxsize > 2**32:
        # 64 bit Python version
        return joblib.load(PIPELINE_64_PATH)
    else:
        # 32 bit Python version
        return joblib.load(PIPELINE_64_PATH)
    
def predict_D12(data_df):
    """Use loaded model to make a prediction. Input is a dataframe."""
    pipeline = load_pipeline()
    y_pred = pipeline.predict(data_df)
    return y_pred


def print_results(results):
    """Prints results to command line"""
    print('\nPredicted diffusivities:')
    for i, d12 in enumerate(results):
        print(f'D12({i+1}) = {d12:.8E} cm2/s')


def save_to_csv(results, data, filename):
    """Output results to CSV file"""
    d12_df = pd.DataFrame({'D12pred': results})
    data['D12pred'] = d12_df['D12pred']
    data.to_csv(filename)
    print(f'Results saved to {filename}.\n')


def main():
    """Program entry point and argument parsing."""
    # Instantiate the parser
    parser = argparse.ArgumentParser(prog='ml_polar', description='Polar systems diffusivity estimator')

    # Providing the 6 properties as ordered list
    parser.add_argument('-p',
                        '--properties',                         
                        action='store', 
                        type=float, 
                        nargs=6, 
                        metavar=('TEMPERATURE', 'VISCOSITY', 'SOLUTE_MOLECULAR_MASS', 'SOLUTE_CRITICAL_PRESSURE', 'SOLVENT_MOLECULAR_MASS', 'SOLVENT_LENNARD_JONES_ENERGY'),
                        help='Temperature (K), Viscosity (cp), Solute molecular mass (g/mol), Solute critical pressure (bar), solvent molecular mass (g/mol), solvent Lennard-Jones energy (K). Provided in this order.')

    # Providing the 6 properties individually
    parser.add_argument('-t', '--temperature', type=float, help='Temperature in K')
    parser.add_argument('-v', '--viscosity', type=float, help='Viscosity in cp')
    parser.add_argument('-m2', '--solutemolecularmass', type=float, help='Solute molecular mass in g/mol')
    parser.add_argument('-cp2', '--solutecriticalpressure', type=float, help='Solute critical pressure in bar')
    parser.add_argument('-m1', '--solventmolecularmass', type=float, help='Solvent molecular mass in g/mol')
    parser.add_argument('-e1', '--solventlennardjonesenergy', type=float, help='Solvent Lennard-Jones energy in K')

    # Providing a file with data
    parser.add_argument('-f', '--csvfile', type=str, help='Path to CSV file with input data')

    # Save results to file
    parser.add_argument('-s', '--save', action='store_true', help='Save results to file')

    # Parse arguments
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.error('No arguments provided.')

    if args.properties:
        if len(args.properties) != 6:
            parser.error('You must provide the 5 properties in the correct order: temperature, viscosity, solutemolecularmass, solutecriticalpressure, solventmolecularmass, and solventlennardjonesenergy.')

        # Create a single point Dataframe
        data = {
            'T': [args.properties[0]],
            'viscosity': [args.properties[1]],
            'solute.M2': [args.properties[2]],
            'solute.Pc': [args.properties[3]],
            'solvent.M1': [args.properties[4]],
            'solvent.elj': [args.properties[5]]
        }
        df = pd.DataFrame.from_dict(data)

    elif (args.temperature or args.viscosity or args.solutemolecularmass or args.solutecriticalpressure or args.solventmolecularmass or args.solventlennardjonesenergy):
        if not (args.temperature and args.viscosity and args.solutemolecularmass and args.solutecriticalpressure and args.solventmolecularmass and args.solventlennardjonesenergy):
            parser.error('All parameters must be provided when specifying one of --temperature, --viscosity, --solutemolecularmass, --solutecriticalpressure, --solventmolecularmass, or --solventlennardjonesenergy.')

        # Create a single point Dataframe
        data = {
            'T': [args.temperature],
            'viscosity': [args.viscosity],
            'solute.M2': [args.solutemolecularmass],
            'solute.Pc': [args.solutecriticalpressure],
            'solvent.M1': [args.solventmolecularmass],
            'solvent.elj': [args.solventlennardjonesenergy]
        }
        df = pd.DataFrame.from_dict(data)

    elif args.csvfile:
        if not os.path.isfile(args.csvfile):
            parser.error('The file does not exist. Make sure to include the file extension (.csv)')
        
        # Load CSV file into dataframe
        data = pd.read_csv(args.csvfile, sep=';|,', engine='python')  

        # Select relevant columns
        df = data[MODEL_VARIABLES]

    # Make calculations (predictions)
    d12_pred = predict_D12(df)
    
    # Print results to comand line
    print_results(d12_pred)

    # Save to CSV
    if args.save:
        save_to_csv(d12_pred, df, OUTPUT_FILE_PATH)


def calc_D12(temperature, viscosity, solutemolarmass, solutecriticalpressure, solventmolarmass, solventLJenergy):
    # Create a single point Dataframe
    data = {
        'T': [temperature],
        'viscosity': [viscosity],
        'solute.M2': [solutemolarmass],
        'solute.Pc': [solutecriticalpressure],
        'solvent.M1': [solventmolarmass],
        'solvent.elj': [solventLJenergy],
    }
    df = pd.DataFrame.from_dict(data)

    # Make calculations (predictions)
    d12_pred = predict_D12(df)

    return d12_pred


if __name__ == '__main__':
    main()
