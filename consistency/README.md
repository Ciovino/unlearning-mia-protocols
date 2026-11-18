# Consistency across Retain-based repeats
One row per configuration (size $\times$ variant $\times$ model $\times$ attack $\times$ classifier).
- `mad_*`, `kappa_*`, `pabak_*`: mean and std over the 10 pairs of repeats (MAD on the probabilities, κ and PABAK on the per-repeat decisions).
- `std`: standard deviation of the AMR across the five repeats.
- `amr_repeat_min`, `amr_repeat_max`: lowest and highest per-repeat AMR.
- `amr_lo`, `amr_hi`: 95% identity-level bootstrap interval of the AMR.
