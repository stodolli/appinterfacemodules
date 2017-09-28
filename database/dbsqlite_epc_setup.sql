-- Set up the NCP/EP protein models

CREATE TABLE protein_models (
  protein_model_id INTEGER PRIMARY KEY,
  protein_model_name TEXT UNIQUE NOT NULL,
  model_pdb_id TEXT NOT NULL,
  dna_bpsteps_num INTEGER NOT NULL,
  binding_domain_start INTEGER NOT NULL,
  binding_domain_end INTEGER NOT NULL,
  bindingframe_o_x REAL NOT NULL,
  bindingframe_o_y REAL NOT NULL,
  bindingframe_o_z REAL NOT NULL,
  bindingframe_x_x REAL NOT NULL,
  bindingframe_x_y REAL NOT NULL,
  bindingframe_x_z REAL NOT NULL,
  bindingframe_y_x REAL NOT NULL,
  bindingframe_y_y REAL NOT NULL,
  bindingframe_y_z REAL NOT NULL,
  bindingframe_z_x REAL NOT NULL,
  bindingframe_z_y REAL NOT NULL,
  bindingframe_z_z REAL NOT NULL,
  startframe_o_x REAL,
  startframe_o_y REAL,
  startframe_o_z REAL,
  startframe_x_x REAL,
  startframe_x_y REAL,
  startframe_x_z REAL,
  startframe_y_x REAL,
  startframe_y_y REAL,
  startframe_y_z REAL,
  startframe_z_x REAL,
  startframe_z_y REAL,
  startframe_z_z REAL,
  endframe_o_x REAL,
  endframe_o_y REAL,
  endframe_o_z REAL,
  endframe_x_x REAL,
  endframe_x_y REAL,
  endframe_x_z REAL,
  endframe_y_x REAL,
  endframe_y_y REAL,
  endframe_y_z REAL,
  endframe_z_x REAL,
  endframe_z_y REAL,
  endframe_z_z REAL,
  fixed_charges_num INTEGER NOT NULL,
  mobile_charges_num INTEGER NOT NULL,
  mobile_tail_charge FLOAT,
  mobile_tail_map TEXT
);

CREATE TABLE protein_model_bpsteps (
  bpstep_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  tilt REAL NOT NULL,
  roll REAL NOT NULL,
  twist REAL NOT NULL,
  shift REAL NOT NULL,
  slide REAL NOT NULL,
  rise REAL NOT NULL,
  FOREIGN KEY (protein_model_id) REFERENCES protein_models(protein_model_id)
);

CREATE TABLE protein_model_bpframes (
  bpframe_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  origin_x REAL NOT NULL,
  origin_y REAL NOT NULL,
  origin_z REAL NOT NULL,
  x_x REAL NOT NULL,
  x_y REAL NOT NULL,
  x_z REAL NOT NULL,
  y_x REAL NOT NULL,
  y_y REAL NOT NULL,
  y_z REAL NOT NULL,
  z_x REAL NOT NULL,
  z_y REAL NOT NULL,
  z_z REAL NOT NULL,
  FOREIGN KEY (protein_model_id) REFERENCES protein_models(protein_model_id)
);

CREATE TABLE protein_model_charges (
  point_charge_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  charge REAL NOT NULL,
  local_x REAL NOT NULL,
  local_y REAL NOT NULL,
  local_z REAL NOT NULL,
  FOREIGN KEY (protein_model_id) REFERENCES protein_models(protein_model_id)
);


-- Set up simulation data

CREATE TABLE simulations (
  simulation_id INTEGER PRIMARY KEY,
  simulation_description TEXT NOT NULL,
  simulation_part INTEGER,
  nrl INTEGER NOT NULL,
  dnasteps_num INTEGER NOT NULL,
  proteins_num INTEGER NOT NULL,
  unbound_dnalinkers_num INTEGER NOT NULL,
  ep_proteins BOOLEAN NOT NULL,
  mc_simulation_type TEXT,
  mc_sampler_type TEXT NOT NULL,
  mc_protein_sampling_frequency REAL NOT NULL,
  mc_sampling_amplitude REAL,
  mc_temperature REAL,
  dna_model_preset TEXT,
  potential_model_preset TEXT,
  endtoend_dist_filter REAL,
  start_date DATETIME,
  end_date DATETIME,
  simulation_input TEXT,
  starting_config TEXT,
  average_steps TEXT,
  simulation_log TEXT,
  snapshots_zip_path TEXT
);

CREATE TABLE structures (
  structure_id INTEGER PRIMARY KEY,
  simulation_id INTEGER NOT NULL,
  energy REAL NOT NULL,
  endtoend_x REAL NOT NULL,
  endtoend_y REAL NOT NULL,
  endtoend_z REAL NOT NULL,
  endtoend_dist REAL NOT NULL,
  ep_distance REAL,
  radius_gyration REAL,
  sedimentation_coeff REAL,
  total_overlap REAL,
  FOREIGN KEY (simulation_id) REFERENCES simulations(simulation_id)
);

CREATE TABLE proteins (
  protein_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  structure_id INTEGER NOT NULL,
  protein_index INTEGER NOT NULL,
  origin_x REAL NOT NULL,
  origin_y REAL NOT NULL,
  origin_z REAL NOT NULL,
  x_x REAL NOT NULL,
  x_y REAL NOT NULL,
  x_z REAL NOT NULL,
  y_x REAL NOT NULL,
  y_y REAL NOT NULL,
  y_z REAL NOT NULL,
  z_x REAL NOT NULL,
  z_y REAL NOT NULL,
  z_z REAL NOT NULL,
  FOREIGN KEY (protein_model_id) REFERENCES protein_models(protein_model_id),
  FOREIGN KEY (structure_id) REFERENCES structures(structure_id)
);

CREATE TABLE local_half_linkers(
  linker_id INTEGER PRIMARY KEY,
  protein_id INTEGER NOT NULL,
  linker_index INTEGER NOT NULL,
  linker_type TEXT NOT NULL,
  angle_a REAL,
  angle_b REAL,
  midpoint_x REAL,
  midpoint_y REAL,
  midpoint_z REAL,
  endpoint_x REAL,
  endpoint_y REAL,
  endpoint_z REAL,
  FOREIGN KEY (protein_id) REFERENCES proteins(protein_id)
);

CREATE TABLE dnasteps (
  bpstep_id INTEGER PRIMARY KEY,
  structure_id INTEGER NOT NULL,
  linker_id INTEGER NOT NULL,
  linker_index INTEGER NOT NULL,
  tilt REAL NOT NULL,
  roll REAL NOT NULL,
  twist REAL NOT NULL,
  shift REAL NOT NULL,
  slide REAL NOT NULL,
  rise REAL NOT NULL,
  twist_energy REAL,
  bend_energy REAL,
  FOREIGN KEY (structure_id) REFERENCES structures(structure_id),
  FOREIGN KEY (linker_id) REFERENCES local_half_linkers(linker_id)
);

-- CREATE TABLE dnaframes (
--   dnaframe_id INTEGER NOT NULL PRIMARY KEY,
--   dnastep_id INTEGER NOT NULL,
--   structure_id INTEGER NOT NULL,
--   origin_x REAL,
--   orign_y REAL,
--   origi_z REAL,
--   x_x REAL,
--   x_y REAL,
--   x_z REAL,
--   y_x REAL,
--   y_y REAL,
--   y_z REAL,
--   z_x REAL,
--   z_y REAL,
--   z_z REAL,
--   FOREIGN KEY (dnastep_id) REFERENCES dnasteps(dnastep_id),
--   FOREIGN KEY (structure_id) REFERENCES structures(structure_id)
-- );

CREATE TABLE histone_tails (
  tail_id INTEGER PRIMARY KEY,
  protein_id INTEGER NOT NULL,
  histone_type TEXT NOT NULL,
  charge REAL NOT NULL,
  local_x REAL NOT NULL,
  local_y REAL NOT NULL,
  local_z REAL NOT NULL,
  global_x REAL,
  global_y REAL,
  global_z REAL,
  FOREIGN KEY (protein_id) REFERENCES proteins(protein_id)
);

CREATE TABLE protein_interactions (
  interaction_id INTEGER PRIMARY KEY,
  protein1_id INTEGER NOT NULL,
  protein2_id INTEGER NOT NULL,
  distance REAL NOT NULL,
  face_overlap REAL,
  side_overlap REAL,
  face_side_overlap REAL,
  FOREIGN KEY (protein1_id) REFERENCES proteins(protein_id),
  FOREIGN KEY (protein2_id) REFERENCES proteins(protein_id)
);