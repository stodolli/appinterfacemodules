CREATE TABLE simulations (
  simulation_id INTEGER PRIMARY KEY,
  simulation_description TEXT NOT NULL,
  nrl INTEGER NOT NULL,
  dnasteps_num INTEGER NOT NULL,
  proteins_num INTEGER NOT NULL,
  unbound_dnalinkers_num INTEGER NOT NULL,
  ep_proteins BOOLEAN NOT NULL,
  mc_simulation_type TEXT,
  mc_sampler_type TEXT NOT NULL,
  mc_sampling_amplitude REAL,
  mc_temperature REAL,
  dna_model_preset TEXT,
  potential_model_preset TEXT,
  endtoend_dist_filter REAL,
  timestamp DATETIME,
  starting_config TEXT,
  simulation_log TEXT,
  snapshots_zip_path TEXT
);

CREATE TABLE structures (
  structure_id INTEGER PRIMARY KEY,
  simulation_id INTEGER NOT NULL,
  energy REAL NOT NULL,
  endtoend_dist REAL NOT NULL,
  radius_gyration REAL NOT NULL,
  sedimentation_coeff REAL,
  total_overlap REAL,
  FOREIGN KEY (simulation_id) REFERENCES simulations(simulation_id)
);

CREATE TABLE dnasteps (
  bpstep_id INTEGER PRIMARY KEY,
  structure_id INTEGER NOT NULL,
  linker_index INTEGER NOT NULL,
  tilt REAL NOT NULL,
  roll REAL NOT NULL,
  twist REAL NOT NULL,
  shift REAL NOT NULL,
  slide REAL NOT NULL,
  rise REAL NOT NULL,
  energy REAL,
  FOREIGN KEY (structure_id) REFERENCES structures(structure_id)
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

CREATE TABLE protein_models (
  protein_model_id INTEGER PRIMARY KEY,
  model_name TEXT NOT NULL,
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
  fixed_charges_num INTEGER NOT NULL,
  mobile_charges_num INTEGER NOT NULL
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

CREATE TABLE protein_model_charges (
  point_charge_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  charge REAL NOT NULL,
  local_x REAL NOT NULL,
  local_y REAL NOT NULL,
  local_z REAL NOT NULL,
  FOREIGN KEY (protein_model_id) REFERENCES protein_models(protein_model_id)
);

CREATE TABLE proteins (
  protein_id INTEGER PRIMARY KEY,
  protein_model_id INTEGER NOT NULL,
  structure_id INTEGER NOT NULL,
  origin_x REAL NOT NULL,
  orign_y REAL NOT NULL,
  origi_z REAL NOT NULL,
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

CREATE TABLE histonetails (
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

-- CREATE TABLE ncpoverlaps (
--
-- );