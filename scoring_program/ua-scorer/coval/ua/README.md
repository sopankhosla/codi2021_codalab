# Using CoVal for evaluating the UA format


## Usage

The following command evaluates coreference outputs related to the UA format:

python ua-scorer.py key system [options]

'key', 'system' are the location of key and system files.


## Evaluation Metrics

The above command reports MUC [Vilain et al, 1995], B-cubed [Bagga and Baldwin, 1998], CEAF [Luo et al., 2005], LEA [Moosavi and Strube, 2016] and the averaged CoNLL score (the average of the F1 values of MUC, B-cubed and CEAFe) [Denis and Baldridge, 2009a; Pradhan  et  al., 2011].

You can also only select specific metrics by including one or some of the 'muc', 'bcub', 'ceafe', 'ceafm', 'blanc' and 'lea' options in the input arguments.
For instance, the following command only reports the CEAFe and LEA scores:

python ua-scorer.py key system ceafe lea

The first and second arguments after 'ua-scorer.py' have to be 'key' and 'system', respectively. The order of other options is arbitrary.

## Evaluation Modes

Apart from coreference relations, the UA dataset also contains annotations for singletons, non-referring, split-antecedent, bridging and discouse-deixis markables. Non-referring markables are annotated within the identity column with EntityIDs ends with '-Pseudo' tag and are therefore distinguishable from referring markables (coreferent markables or singletons). Split-antecedent is also marked in the identity column using 'Element-of' key in the antecedents.
Bridging and discouse-deixis are annotated in a separate column.
After extracting all markables, all markables whose corresponding coreference chain is of size one, are specified as singletons.
By distinguishing coreferent markables, singletons, bridging, split-antecedent and non-referring markables, we can perform coreference evaluations in various settings by using the following two options:

1) remove_singletons:  if this option is included in the command, all singletons in the key and system files will be excluded from the evaluation. 
The handling of singletons

2) remove_split_antecedent: if this option is included in the command, all split-antecedent in the key and system files will be excluded from the evaluation.
The handling of singletons

3) keep_non_referring:  if this option is included in the command, all markables that are annotated as non_referring, both in the key and system files, will be included in the evaluation.
If this option is included, separate recall, precision, and F1 scores would be reported for identifying the annotated non-referring markables.

4) keep_bridging: if this option is included in the command, all markables that are annotated as bridging, both in the key and system files, will be included in the evaluation.
If this option is included, separate recall, precision, and F1 scores would be reported for identifying the annotated bridging markables.

5) evaluate_discourse_deixis: if this option is included in the command the scorer will only evaluate the discouse deixis using the metrics specified.

6) only_split_antecedent: there is also an option to only assess the quality of the alignment between the split-antecedents in the key and system.

As a result, if you only run 'python arrau-scorer.py key system' without any additional options, the evaluation is performed by incorporating all coreferent, split-antecedent and singleton markables and without considering non-referring, bridging or discourse-deixis markables.

Overall, the above options enable the following evaluation modes:

# Evaluating coreference relations only

This evaluation mode is compatible with the coreference evaluation of the OntoNotes dataset in which only coreferring markables are evaluated.
To do so, the remove_singletons option should be included in the evaluation command:

python ua-scorer.py key system remove_singletons remove_split_antecedent

In this mode, all split-antecedent, singletons, bridging, discourse-deixis and non-referring mentions will be skipped from coreference evaluations.

# Evaluating coreference relations (include split-antecedents) and singletons

This is the default evaluation mode of the ua dataset and its corresponding command is

python ua-scorer.py key system

In this mode, both coreferring markables, split-antecedents and singletons are evaluated by the specified evaluation metrics.
Apart from the MUC metric, all other evaluation metrics handle singletons.
The only case in which MUC handles singletons is when they are incorrectly included in system detected coreference chains. In this case, MUC penalizes the output for including additional incorrect coreference relations. Otherwise, MUC does not handle, or in other words skip, markables that do not have coreference links. 
You can refer to Moosavi and Strube [2016] for more details about various evaluation metrics.

# Evaluating all markables (exclude discourse-deixis)

In this evaluation setting, all specified markables including coreference, split-antecedents, singleton, bridging and non-referring mentions are taken in to account for evaluation.
The scores of coreference evaluation metrics would be the same as those of the above mode, i.e. evaluating coreference relations, split-antecedents and singletons.
However, separate scores would be reported for identifying the annotated non-referring markables and bridging relations.

The following command performs coreference evaluation using this mode

python ua-scorer.py key system keep_non_referring keep_bridging

# Evaluating discourse-deixis

In this evaluation setting only the discouse-deixis will be evaluated.

The following command performs coreference evaluation using this mode

python ua-scorer.py key system evaluate_discourse_deixis

# Evaluating only split-antecedent alignment
In this evaluation setting only split-antecedents will be evaluated, the scores are reported according to the alignment between split-antecedents in the key and system predictions.

The following command performs coreference evaluation using this mode

python ua-scorer.py key system only_split_antecedent
 
## Minimum Span Evaluation

The UA dataset may contain a MIN attribute which indicates the minimum string that a coreference
resolver must identify for the corresponding markable.
For minimum span evaluation, a system detected boundary for a markable is considered as correct if it contains the MIN string and doesn't go beyond the annotated maximum boundary.

To perform minimum span evaluations, add one of the 'MIN', 'min' or 'min_spans' options to the input arguments.
For instance, the following command reports all standard evaluation metrics using minimum spans to specify markables instead of maximum spans:

python ua-scorer.py key system min

