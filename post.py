import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def post_processing(inputs,params,sol):

    # Post-processing:
    # Find final z locations
    z = np.zeros(inputs.Nz)
    dz = params['dz_0'] + sol.y[:,-1]/inputs.rho_w
    
    z[0] = dz[0]/2
    for i in range(inputs.Nz-1):
        z[i+1] = z[i] + dz[i]/2 + dz[i+1]/2
    
    # Find dz and z vectors for each time step
    z_t = np.zeros_like(sol.y)
    dz_t = np.zeros_like(sol.y)
    
    for i in range(sol.t.size):
        dz_t[:,i] = params['dz_0'] + sol.y[:,i]/inputs.rho_w
        
    z_t[0,:] = dz_t[0,:]/2
    for j in range(sol.t.size):
        for i in range(inputs.Nz-1):
            z_t[i+1,j] = z_t[i,j] + dz_t[i,j]/2 + dz_t[i+1,j]/2
        
    # Final film thickness
    z_f = z[-1] + dz[-1]/2
    y_lo = np.round(0.8*np.min(sol.y[:,-1]/dz_t[:,-1]),1)
    y_hi = np.round(1.2*np.max(sol.y[:,-1]/dz_t[:,-1]),1)
    
    # Evaluate total mass/area vs. time from sv of densities
    #   ... using a weighted average b/c dz differences?
    M_tot = np.zeros_like(sol.t)
    for i in range(sol.t.size):
        M_tot[i] = sum(sol.y[:,i]*dz_t[:,i])/sum(dz_t[:,i])
        
    # Evaluate thickness vs. time from sv densities
    h_tot = np.zeros_like(sol.t)
    for i in range(sol.t.size):
        h_tot[i] = sum(dz_t[:,i])


    
    # Plotting:
    def format_fig(fig,x,y,wd=inputs.wd,ht=inputs.ht,fs=inputs.fs,fn=inputs.fn):
        
        fig.set_size_inches([wd,ht])
        
        ax = fig.gca()
        if all(['data' in x.keys(), 'data' in y.keys()]):
            ax.plot(x['data'],y['data'])
            
        if x.get('label'): ax.set_xlabel(x['label'],fontname=fn,fontsize=fs)
        if y.get('label'): ax.set_ylabel(y['label'],fontname=fn,fontsize=fs)
        
        if x.get('limits'): ax.set_xlim(x['limits'])
        if y.get('limits'): ax.set_ylim(y['limits'])
        
        if x.get('ticks'): ax.set_xticks([x['ticks'][0]+i*x['ticks'][1] for i in range(0,x['ticks'][2])])
        if y.get('ticks'): ax.set_yticks([y['ticks'][0]+i*y['ticks'][1] for i in range(0,y['ticks'][2])])
        
        ax.minorticks_on()
        ax.get_xaxis().set_tick_params('both',direction='in',top=1)
        ax.get_yaxis().set_tick_params('both',direction='in',right=1)
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fs)
            tick.label1.set_fontname(fn)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fs)
            tick.label1.set_fontname(fn)
            
    
    if inputs.plt_flag:
            
        # t index for contour
        # Find the time that it takes to reach 95% of final mass
        M_95 = 0.95*M_tot[-1]
        t_ind = np.argmin(np.abs(M_tot - M_95))
            
            
        # Depth vs. H2O Density for range of times
        spacing = np.linspace(0,1,sol.t[:t_ind].size+1)
        norm = mpl.colors.Normalize(vmin=0,vmax=np.round(sol.t[t_ind]/60))
        c_vec = plt.cm.jet(norm(sol.t[:t_ind]/60))
            
        fig,ax = plt.subplots(nrows=1,ncols=1)
        for i in range(sol.y[:,:t_ind].shape[1]):
            ax.plot(z_t[:,i]*1e9,sol.y[:,i]/dz_t[:,i],color=c_vec[i])
            
        xprops = {'label': 'Film depth (nm)', 'limits': [0,1.05*np.max(h_tot)*1e9]}
        yprops = {'label': r'H$_2$O density (kg/m$^3$)', 'limits': [0,1.1*np.max(np.max(sol.y/dz_t))]}
        format_fig(fig,xprops,yprops)
        
        ax.plot(h_tot*1e9,sol.y[-1,:]/dz_t[-1,:],'-k')
        ax.plot(z_t[:,-1]*1e9,sol.y[:,-1]/dz_t[:,-1],'-k')
        
        clrmap = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.jet)
        clrmap.set_array(sol.t[:t_ind]/60)
        
        cbaxes = fig.add_axes([0.95, 0.17, 0.03, 0.65])
        
        cbar = fig.colorbar(clrmap, cax=cbaxes, orientation='vertical')
        cbar.set_label('Time  (min)', fontsize=inputs.fs, fontname=inputs.fn, labelpad=5)
        cbar.ax.tick_params(axis='y',direction='in')
        cbar.ax.tick_params(pad=3)
        
        # Depth vs. H2O Density at t = t_sim
        fig,ax = plt.subplots(nrows=1,ncols=1)
        xprops = {'data': z_t[:,-1]*1e9, 'label': 'Film depth (nm)', 'limits': [0,1.05*np.max(h_tot)*1e9]}
        yprops = {'data': sol.y[:,-1]/dz_t[:,-1], 'label': r'H$_2$O density (kg/m$^3$)', 'limits': [y_lo,y_hi]}
        format_fig(fig,xprops,yprops)
        
        ax.legend(['t = '+str(sol.t[-1]/60)+' min'],loc='lower left',frameon=False)
        ax.vlines(z_f*1e9,y_lo,y_hi,linestyle='--',color='k')
        
        if inputs.BC_s == 'simple':
            ax.plot(z_f*1e9,inputs.C_eq,'or',zorder=10)
        
        # Time vs. Mass Density
        fig,ax = plt.subplots(nrows=1,ncols=1)
        xprops = {'data': sol.t/60, 'label': 'Time (min)', 'limits': [0,sol.t[-1]/60]}
        yprops = {'data': M_tot*1e8, 'label': r'Mass H$_2$O per area (ng/cm$^2$)', 'limits': [0,1.1*np.max(M_tot)*1e8]}
        format_fig(fig,xprops,yprops)
        
        
        # Time vs. Thickness
        fig,ax = plt.subplots(nrows=1,ncols=1)
        xprops = {'data': sol.t/60, 'label': 'Time (min)', 'limits': [0,sol.t[-1]/60]}
        yprops = {'data': h_tot*1e9, 'label': 'Nafion thickness (nm)', 'limits': [inputs.t_Naf*1e9,np.max(h_tot)*1e9 + 0.1*(np.max(h_tot)*1e9-inputs.t_Naf*1e9)]}
        format_fig(fig,xprops,yprops)
    
    outputs = locals()
    
    return outputs

