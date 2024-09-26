import optuna
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import psycopg2

def objective(trial):
    data, target = load_iris(return_X_y=True) # load dataset

    n_estimators = trial.suggest_int('n_estimators', 2, 100) # hyperparameters to be optimized
    max_depth = trial.suggest_int('max_depth', 4, 64, log=True)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 16)

    # classifier with these hyperparameters
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split
    )

    # Evaluate using cross-validation
    return cross_val_score(clf, data, target, n_jobs=-1, cv=3).mean()


study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=1000)

best_trial = study.best_trial
print("Best trial:", best_trial)
print("Best parameters:", study.best_params)
print("Best value:", study.best_value)

print(study.trials_dataframe())

optuna.visualization.plot_optimization_history(study)
optuna.visualization.plot_param_importances(study)

pruner = study.pruner
#study = optuna.load_study(study_name="optuna_trial_1", storage="postgresql://postgres:%40password%40localhost:5432/optuna")





