# pull-request

Prepares, reviews, updates, pushes, and creates GitHub pull requests from local branch work, defaulting to draft PRs unless requested otherwise.

## Optional label configuration

The skill does not add, remove, or propose labels unless `references/labels.local.json` is present and valid. This ignored local file lets each organisation define its own labels without making the skill organisation-specific.

Create the file with a JSON object containing a `labels` array. Each entry needs a label name, category, and short meaning:

```json
{
  "labels": [
    {
      "label": "bug",
      "category": "change-type",
      "meaning": "Fixes a defect."
    }
  ]
}
```

Add only labels that exist in the target repository. Keep the file local: it is ignored by Git and must not be committed.
