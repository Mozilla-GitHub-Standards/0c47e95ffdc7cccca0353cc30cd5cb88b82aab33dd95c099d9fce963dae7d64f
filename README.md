# Hasal_analysis
The spent time of each component. (from Hasal)

## Commands

* ascii_diag_generator.py
  * generate ASCII diagram
  * `$ python ascii_diag_generator.py -s bugzilla/<BUG_ID>`

* `make template`
  * generate template folder structrue base on `summary/*/` folders.

* `make summary`
  * generate the `output/summary.json` file.

* `make clean`
  * clean files under `output` folder.

## Folders

* bugzilla
  * Time and percentage of methods of each bugs.
  * Each folders under `bugzilla/<BUG_ID>` have the `<NN>.<MM>` file, which means `<NN> ms` and `<MM> %`.
  * ex: it means `836ms 100% Startup::XRE_Main`

    ```
    bugzilla/1269684/
    └── Startup::XRE_Main
        ├── 836.100
    ```

* summary
  * The time analysis of each methods. Should identify the timeunit.
  * The `<FOO>.timeunit` and `<NN>.time` means that `When doing <FOO>, the methods spent <NN> ms`.
  * ex: When `domLoading_to_loadEventEnd`, `nsHtml5TreeOpExecutor::RunFlushLoop > nsJSUtils::EvaluateString` spent `1050 ms`

    ```
    summary/1264535.PageDown_3_Page/
    └── Startup::XRE_Main
        ├── nsHtml5TreeOpExecutor::RunFlushLoop
        │   └── nsJSUtils::EvaluateString
        │       └── domLoading_to_loadEventEnd.timeunit
        │           └── 1050.time
    ```

* template
  * Golden templat methods call structure.
