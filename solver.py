import numpy as np
from scipy.integrate import solve_ivp

def main_solver(inputs,params):

    # Modeling equations:
    def dsvdt_func(t,sv,p):
        
        # sv is water mass per area [kg/m^2] for each CV node
        dsvdt = np.zeros_like(sv)
        
        # instantaneous swelling:
        #   dz [m] -> CV thicknesses, 
        #   dz_av [m] -> distance between node centers
        dz = p['dz_0'] + sv/inputs.rho_w
        dz_av = dz[0:inputs.Nz-1]/2 + dz[1:inputs.Nz]/2
        
        # Concentrations at each node:
        #   C_upr [kg/m^3] -> mass concentrations of nodes 1:end, 
        #   C_lwr [kg/m^3] -> mass concentrations of nodes 0:end-1
        C_upr = sv[1:inputs.Nz]/dz[1:inputs.Nz]
        C_lwr = sv[0:inputs.Nz-1]/dz[0:inputs.Nz-1] 
        
        # no flux BC, lower boundary fluxes
        J_bot = np.hstack([0.,inputs.D_H2O*(C_lwr - C_upr)/dz_av])  
    
        # top boundary fluxes, rxn BC
        if inputs.BC_s == 'simple':
            s_dot = inputs.r_rxn*(inputs.C_eq - sv[-1]/dz[-1])
        elif inputs.BC_s == 'cantera':
            Y_h2o = sv[-1] / (sv[-1] + 1980*p['dz_0'])
            p['naf_b'].Y = {'H(Naf)': 1.-Y_h2o, 'O2(Naf)': 0., 'H2O(Naf)': Y_h2o}
            n_dot = p['naf_s'].get_net_production_rates(p['naf_b'])
            s_dot = n_dot[p['ih2o_n']]*p['naf_b'].molecular_weights[p['ih2o_n']]
        else:
            raise NotImplementedError('invalid input for BC_s...')
            
        # print(s_dot)
        J_top = np.hstack([inputs.D_H2O*(C_upr - C_lwr)/dz_av,s_dot])                      
        
        # derivative expression
        dsvdt = J_bot + J_top    
        
        return dsvdt
    
    sol = solve_ivp(lambda t,sv: dsvdt_func(t,sv,params),[0.,inputs.t_sim],params['sv_0'],
                    method=inputs.method,atol=inputs.atol,rtol=inputs.rtol)
    
    # print(params['naf_b'].Y)
    
    return sol

if __name__ == '__main__':
    pass