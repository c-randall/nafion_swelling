# Import necessary modules:
import pandas as pd
import cantera as ct

from pre import pre_processing
from solver import main_solver
from post import post_processing

def make_lalign_formatter(df, cols=None):
    """
    Construct formatter dict to left-align columns.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The DataFrame to format
    cols : None or iterable of strings, optional
        The columns of df to left-align. The default, cols=None, will
        left-align all the columns of dtype object

    Returns
    -------
    dict
        Formatter dictionary

    """
    if cols is None:
       cols = df.columns[df.dtypes == 'object']

    return {col: f'{{:<{df[col].str.len().max()}s}}'.format for col in cols}

# Inputs:
class simulation():
    yamlfile     = 'pemfc.yaml'             # Path to cantera yaml file
    T_gas, P_gas = 30, 1.0*ct.one_atm       # T [C] and P [Pa] for gas
    T_naf, P_naf = 30, 1.0*ct.one_atm       # T [C] and P [Pa] for naf

    Nz    = 100         # Number of z discretizations [-]
    t_Naf = 10e-9       # Dry Nafion thickness [m]
    D_H2O = 2e-18       # Effective H2O diffusion coeff [m^2/s]
    r_rxn = 1e-8        # Simple absorption/desorption coefficient [m/s]
    k_fwd = 5e-6        # Cantera forward reaction constant [m/s]
    t_sim = 300.        # Simulation time [s]
    rho_0 = 0.          # Initial H2O mass concentation [kg/m^3]
    rho_w = 1e3         # Density of pure water [kg/m^3]
    C_eq  = 2e2         # Equilibrium mass concentration [kg/m^3]
    RH_g  = 90.         # Gas-phase relative humidity [%]
    Y_h2o = 0.          # Initial mass fraction of H2O(N) [-]
    BC_s  = 'cantera'   # Nafion-gas boundary condition...
                        #   'simple': alpha*(C_eq-C_top),
                        #   'cantera': naf_s.get_net_production_rates()

    method = 'BDF'      # solve_ivp method, check online documentation [-]
    atol = 1e-9         # Absolute tolerance [kg/m^2]
    rtol = 1e-4         # Relative tolerance [-]

    plt_flag = True     # turn on/off plots
    ht = 2              # fig height [in]
    wd = 3              # fig width [in]
    fs = 12             # fontsize [pt]
    fn = 'Times'        # fontname

    __help_dict = {}
    __help_dict['yamlfile']   = 'Path to cantera yaml file'
    __help_dict['T_gas']      = 'T [C] for gas phase'
    __help_dict['P_gas']      = 'P [Pa] for gas phase'
    __help_dict['T_naf']      = 'T [C] for naf phase'
    __help_dict['P_naf']      = 'P [Pa] for naf phase'
    __help_dict['Nz']         = 'Number of z discretizations [-]'
    __help_dict['t_Naf']      = 'Dry Nafion thickness [m]'
    __help_dict['D_H2O']      = 'Effective H2O diffusion coeff [m^2/s]'
    __help_dict['r_rxn']      = 'Simple absorption/desorption coefficient [m/s]'
    __help_dict['k_fwd']      = 'Cantera forward reaction constant [m/s]'
    __help_dict['t_sim']      = 'Simulation time [s]'
    __help_dict['rho_0']      = 'Initial H2O mass concentation [kg/m^3]'
    __help_dict['rho_w']      = 'Density of pure water [kg/m^3]'
    __help_dict['C_eq']       = 'Equilibrium mass concentration [kg/m^3]'
    __help_dict['RH_g']       = 'Gas-phase relative humidity [%]'
    __help_dict['Y_h2o']      = 'Initial mass fraction of H2O(N) [-]'
    __help_dict['BC_s']       = 'Boundary condition: "simple" or "cantera"'
    __help_dict['method']     = 'Method for solve_ivp (from scipy.integrate)'
    __help_dict['atol']       = 'Absolute tolerance [kg/m^2]'
    __help_dict['rtol']       = 'Relative tolerance [-]'
    __help_dict['plt_flag']   = 'Turn on/off post processing plots, bool'
    __help_dict['ht']         = 'Figure height [in]'
    __help_dict['wd']         = 'Figure width [in]'
    __help_dict['fs']         = 'Figure font size [pt]'
    __help_dict['fn']         = 'Figure font name'

    __help_dict['exp_deets']  = 'Experimental details, dict to overwrite default attr'
    __help_dict['pre_func']   = 'Method to run pre processing, returns params'
    __help_dict['solve_func'] = 'Method to solve simulation, returns sol'
    __help_dict['post_func']  = 'Method to run post processing, returns outputs'
    __help_dict['run']        = 'Run the full simulation: pre, solve, and post'

    __help_dict['params']     = 'Parameters dictionary from pre processing'
    __help_dict['sol']        = 'Solution object from solver function'
    __help_dict['outputs']    = 'Outputs dictionary from post processing'

    __help_dict['help_dict']  = 'Dictionary describing attributes/methods'

    def exp_deets(self,experiment):
        for k in experiment.keys():
            setattr(self, k, experiment[k])

    def pre_func(self):
        self.params = pre_processing(self)

    def solve_func(self):
        self.sol = main_solver(self,self.params)

    def post_func(self):
        self.outputs = post_processing(self,self.params,self.sol)

    def run(self):
        self.pre_func()
        self.solve_func()
        self.post_func()

    def help_dict(self):
        df = pd.DataFrame(columns=('Attribute    ','Description'))
        df.loc[len(df.index)] = ['---------','-----------']

        for i in dir(self):
            if '__' not in i:
                df.loc[len(df.index)] = [i,self.__help_dict[i]]

        print('\n')
        print(df.to_string(formatters=make_lalign_formatter(df),
                           index=False,justify='left'))



if __name__ == '__main__':

    inputs = simulation()
    params = pre_processing(inputs)
    sol = main_solver(inputs,params)
    outputs = post_processing(inputs,params,sol)
