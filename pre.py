import numpy as np
import cantera as ct
from scipy.optimize import fsolve

def pre_processing(inputs):

    # Pre-processing:
    
    # Tabulated T [C] vs. P_sat [kPa] from Engineering Toolbox
    # Link: www.engineeringtoolbox.com/water-vapor-saturation-pressure-d_599.html
    T_dat = np.array([0.01,2,4,10,14,18,20,25,30,34,40,44,50,54,60,70,80,90,
                      96,100,110,120,130,140,150,160,180,200,220,240,260,280,
                      300,320,340,360,370])
    P_dat = np.array([0.61165,0.70599,0.81355,1.2282,1.5990,2.0647,2.3393,
                      3.1699,4.2470,5.3251,7.3849,9.1124,12.352,15.022,19.946,
                      31.201,47.414,70.182,87.771,101.42,143.38,198.67,270.28,
                      361.54,476.16,618.23,1002.8,1554.9,2319.6,3346.9,4692.3,
                      6416.6,8587.9,11284,14601,18666,21044])   
    
    # Function to set gas composition based on RH
    def gas_comp(gas,RH):
        # Get water vapor index from gas object
        ih2o_g = gas.species_index('H2O')
        
        # Interpolated saturation pressure [Pa]
        P_sat = np.interp(gas.T,T_dat+273,P_dat*1e3) 
        
        def comp_func(x_h2o_g):        
            gas.X = {'N2':1.-x_h2o_g, 'O2':0., 'H2O':x_h2o_g}
            P_h2o = gas.P*gas.X[ih2o_g]
            return (P_h2o/P_sat - RH/100.)**2
        
        x_h2o_g = fsolve(comp_func,0.)
        gas.X = {'N2':1.-x_h2o_g, 'O2':0., 'H2O':x_h2o_g}
        P_h2o = gas.P*gas.X[ih2o_g]
        
        print('\nCheck gas state...')
        print('Calculated RH: '+str(np.round(P_h2o/P_sat*100.,0))+'%\n')
    
        return gas 
    
    dz_0 = inputs.t_Naf / inputs.Nz
    
    gas_b = ct.Solution(inputs.yamlfile,'cathode_gas')
    naf_b = ct.Solution(inputs.yamlfile,'naf_bulk_ca')
    naf_s = ct.Interface(inputs.yamlfile,'naf_gas_surf_ca',[naf_b,gas_b])
    
    gas_b.TP = inputs.T_gas+273, inputs.P_gas
    naf_b.TP = inputs.T_naf+273, inputs.P_naf
    naf_s.TP = inputs.T_naf+273, inputs.P_naf
    
    gas_b = gas_comp(gas_b,inputs.RH_g)
    
    ih2o_n = naf_b.species_index('H2O(Naf)')
    naf_b.Y = {'H(Naf)':1.-inputs.Y_h2o, 'O2(Naf)':0., 'H2O(Naf)':inputs.Y_h2o}
    # print(naf_b.Y)
    
    if inputs.BC_s == 'simple':
        sv_0 = np.ones(inputs.Nz)*inputs.rho_0*dz_0
    elif inputs.BC_s == 'cantera':
        H2O_Rxn = naf_s.reaction(1)
        # print(H2O_Rxn.rate.input_data,H2O_Rxn.rate_coeff_units)
        H2O_Rxn.rate = ct.InterfaceArrheniusRate(inputs.k_fwd,0,0)
        naf_s.modify_reaction(1,H2O_Rxn)
        sv_0 = np.ones(inputs.Nz)*1980*inputs.Y_h2o*dz_0 / (1-inputs.Y_h2o)
    else:
        raise NotImplementedError('invalid input for BC_s...')
    
    params = locals()

    return params

if __name__ == '__main__':
    from main import simulation
    
    inputs = simulation()
    params = pre_processing(inputs)