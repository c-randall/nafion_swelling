from main import simulation

# sim0 = simulation()
# sim0.help_dict()
# sim0.run()

sim1 = simulation()
exp1 = {'Y_h2o':0.17, 'RH_g':0}
sim1.exp_deets(exp1)
sim1.run()

# sim2 = simulation()
# exp2 = {'k_fwd':5e-6}
# sim2.exp_deets(exp2)
# sim2.run()

# sim3 = simulation()
# exp3 = {'D_H2O':2e-10}
# sim3.exp_deets(exp3)
# sim3.run()