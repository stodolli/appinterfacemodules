INSERT INTO protein_core_models (
  protein_core_model_name,
  model_pdb_id,
  dna_bpsteps_num,
  binding_domain_start, binding_domain_end,
  bindingframe_o_x, bindingframe_o_y, bindingframe_o_z,
  bindingframe_x_x, bindingframe_x_y, bindingframe_x_z,
  bindingframe_y_x, bindingframe_y_y, bindingframe_y_z,
  bindingframe_z_x, bindingframe_z_y, bindingframe_z_z,
  startframe_o_x, startframe_o_y, startframe_o_z,
  startframe_x_x, startframe_x_y, startframe_x_z,
  startframe_y_x, startframe_y_y, startframe_y_z,
  startframe_z_x, startframe_z_y, startframe_z_z,
  endframe_o_x, endframe_o_y, endframe_o_z,
  endframe_x_x, endframe_x_y, endframe_x_z,
  endframe_y_x, endframe_y_y, endframe_y_z,
  endframe_z_x, endframe_z_y, endframe_z_z,
  core_charges_num
)
VALUES (
  '1KX5_simple_octamer',
  '1KX5',
  146,
  -73, 73,
  40.7, 0.0, 0.0,
  -0.995777, 0.0199155, 0.0896199,
  0.0905211, 0.0502321, 0.994627,
  0.0153067, 0.998539, -0.0518228,
  43.18, 24.99, 20.88,
  -0.460923, -0.801605, -0.380762,
  -0.259323, -0.288669, 0.921641,
  -0.848706, 0.523546, -0.0748209,
  42.82, -25.82, -21.1,
  -0.429635, 0.819304, 0.379677,
  0.189536, -0.329275, 0.925016,
  0.882887, 0.469382, -0.01382,
  26
);

INSERT INTO protein_tails_models (
  protein_tails_model_name, fixed_charges_num,  mobile_charges_num,
  mobile_tail_charge, mobile_tail_map
)
VALUES (
  'simple_tails', 36, 70, 1,
  'H2A1,H2A1,H2A1,H2A1,H2A1,H2A1,H2A1,H2A1,' ||
  'H2B1,H2B1,H2B1,H2B1,H2B1,H2B1,H2B1,H2B1,' ||
  'H31,H31,H31,H31,H31,H31,H31,H31,H31,H31,' ||
  'H41,H41,H41,H41,H41,H41,H41,H41,H41,' ||
  'H2A2,H2A2,H2A2,H2A2,H2A2,H2A2,H2A2,H2A2,' ||
  'H2B2,H2B2,H2B2,H2B2,H2B2,H2B2,H2B2,H2B2,' ||
  'H32,H32,H32,H32,H32,H32,H32,H32,H32,H32,' ||
  'H42,H42,H42,H42,H42,H42,H42,H42,H42'
);

INSERT INTO protein_tails_models (
  protein_tails_model_name, fixed_charges_num,
  mobile_charges_num, mobile_tail_charge, mobile_tail_map
)
VALUES (
  'cg_tails', 8, 34, 2,
  'H2A1,H2A1,H2A1,H2A1,H2B1,H2B1,H2B1,H2B1,' ||
  'H31,H31,H31,H31,H31,H41,H41,H41,H41,' ||
  'H2A2,H2A2,H2A2,H2A2,H2B2,H2B2,H2B2,H2B2,' ||
  'H32,H32,H32,H32,H32,H42,H42,H42,H42'
);



INSERT INTO protein_tails_models (
  protein_tails_model_name, fixed_charges_num, mobile_charges_num,
  mobile_tail_charge, mobile_tail_map
)
VALUES (
  'cg_tails_H3H4', 4, 18, 2,
  'H31,H31,H31,H31,H31,H41,H41,H41,H41,' ||
  'H32,H32,H32,H32,H32,H42,H42,H42,H42'
);

INSERT INTO protein_core_models (
  protein_core_model_name,
  model_pdb_id,
  dna_bpsteps_num,
  binding_domain_start, binding_domain_end,
  bindingframe_o_x, bindingframe_o_y, bindingframe_o_z,
  bindingframe_x_x, bindingframe_x_y, bindingframe_x_z,
  bindingframe_y_x, bindingframe_y_y, bindingframe_y_z,
  bindingframe_z_x, bindingframe_z_y, bindingframe_z_z,
  startframe_o_x, startframe_o_y, startframe_o_z,
  startframe_x_x, startframe_x_y, startframe_x_z,
  startframe_y_x, startframe_y_y, startframe_y_z,
  startframe_z_x, startframe_z_y, startframe_z_z,
  endframe_o_x, endframe_o_y, endframe_o_z,
  endframe_x_x, endframe_x_y, endframe_x_z,
  endframe_y_x, endframe_y_y, endframe_y_z,
  endframe_z_x, endframe_z_y, endframe_z_z,
  fixed_charges_num, mobile_charges_num,
  mobile_tail_charge, mobile_tail_map
)
VALUES (
  '1KX5_octamer_cg_tails_H2AH2B',
  '1KX5',
  146,
  -73, 73,
  40.7, 0.0, 0.0,
  -0.995777, 0.0199155, 0.0896199,
  0.0905211, 0.0502321, 0.994627,
  0.0153067, 0.998539, -0.0518228,
  43.18, 24.99, 20.88,
  -0.460923, -0.801605, -0.380762,
  -0.259323, -0.288669, 0.921641,
  -0.848706, 0.523546, -0.0748209,
  42.82, -25.82, -21.1,
  -0.429635, 0.819304, 0.379677,
  0.189536, -0.329275, 0.925016,
  0.882887, 0.469382, -0.01382,
  30, 16, 2,
  'H2A1,H2A1,H2A1,H2A1,H2B1,H2B1,H2B1,H2B1,' ||
  'H2A2,H2A2,H2A2,H2A2,H2B2,H2B2,H2B2,H2B2'
);

INSERT INTO protein_core_models (
  protein_core_model_name,
  model_pdb_id,
  dna_bpsteps_num,
  binding_domain_start, binding_domain_end,
  bindingframe_o_x, bindingframe_o_y, bindingframe_o_z,
  bindingframe_x_x, bindingframe_x_y, bindingframe_x_z,
  bindingframe_y_x, bindingframe_y_y, bindingframe_y_z,
  bindingframe_z_x, bindingframe_z_y, bindingframe_z_z,
  startframe_o_x, startframe_o_y, startframe_o_z,
  startframe_x_x, startframe_x_y, startframe_x_z,
  startframe_y_x, startframe_y_y, startframe_y_z,
  startframe_z_x, startframe_z_y, startframe_z_z,
  endframe_o_x, endframe_o_y, endframe_o_z,
  endframe_x_x, endframe_x_y, endframe_x_z,
  endframe_y_x, endframe_y_y, endframe_y_z,
  endframe_z_x, endframe_z_y, endframe_z_z,
  fixed_charges_num, mobile_charges_num
)
VALUES (
  '1KX5_octamer_no_tails',
  '1KX5',
  146,
  -73, 73,
  40.7, 0.0, 0.0,
  -0.995777, 0.0199155, 0.0896199,
  0.0905211, 0.0502321, 0.994627,
  0.0153067, 0.998539, -0.0518228,
  43.18, 24.99, 20.88,
  -0.460923, -0.801605, -0.380762,
  -0.259323, -0.288669, 0.921641,
  -0.848706, 0.523546, -0.0748209,
  42.82, -25.82, -21.1,
  -0.429635, 0.819304, 0.379677,
  0.189536, -0.329275, 0.925016,
  0.882887, 0.469382, -0.01382,
  26, 0
);

INSERT INTO protein_core_models (
  protein_core_model_name,
  model_pdb_id,
  dna_bpsteps_num,
  binding_domain_start, binding_domain_end,
  bindingframe_o_x, bindingframe_o_y, bindingframe_o_z,
  bindingframe_x_x, bindingframe_x_y, bindingframe_x_z,
  bindingframe_y_x, bindingframe_y_y, bindingframe_y_z,
  bindingframe_z_x, bindingframe_z_y, bindingframe_z_z,
  core_charges_num
)
VALUES (
  'RNAP',
  '1L9Z',
  30,
  0, 30,
  -63.0085, 7.03573, 22.8533,
  0.739259, -0.0694268, -0.669833,
  0.292893, 0.928813, 0.226982,
  0.60639, -0.363988, 0.706968,
  39
);

INSERT INTO protein_core_models (
  protein_core_model_name,
  model_pdb_id,
  dna_bpsteps_num,
  binding_domain_start, binding_domain_end,
  bindingframe_o_x, bindingframe_o_y, bindingframe_o_z,
  bindingframe_x_x, bindingframe_x_y, bindingframe_x_z,
  bindingframe_y_x, bindingframe_y_y, bindingframe_y_z,
  bindingframe_z_x, bindingframe_z_y, bindingframe_z_z,
  core_charges_num
)
VALUES (
  'NTRC',
  'NtrC',
  26,
  0, 26,
  48.8509, -9.14374, -30.1658,
  0.485977, 0.424388, 0.764016,
  0.84235, 0.00557724, -0.538902,
  -0.232965, 0.905463, -0.354773,
  12
);
