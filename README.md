# Hasal_analysis
The spent time of each component. (from Hasal)

## Commands

* `make ascii bugzilla/<BUG_ID>.<TIMEUNIT>`
  * generate ASCII diagram
  * or `$ python ascii_diag_generator.py -s bugzilla/<BUG_ID>.<TIMEUNIT>`

* `make template`
  * generate template folder structure base on `summary/*/` and `bugzilla/*/` folders.

* `make bug2sum-all`
  * generate the `summary` base on the data under `bugzilla` folder.

* `make summary`
  * generate the `output/summary.json` and `output/summary.xmind` files.

* `make clean`
  * clean files under `output` folder.

## Folders

* bugzilla
  * Time and percentage of methods of each bugs.
  * Each folders under `bugzilla/<BUG_ID>` have the `<NN>.<MM>` file, which means `<NN> ms` and `<MM> %`.
  * ex: it means `836ms 100% Startup::XRE_Main`
  * String after <BUG_ID> means the time unit

    ```
    bugzilla/1269684.font_bold/
    └── Startup::XRE_Main
        ├── 836.100
    ```

* summary
  * The time analysis of each methods. Should identify the timeunit.
  * The `<FOO>.timeunit` and `<NN>.time` means that `When doing <FOO>, the methods spent <NN> ms`.
  * If there are more than one results have the same time, the `<NN>.time.1`, `<NN>.time.2` ... etc are accepted.
  * ex: When `domLoading_to_loadEventEnd`, `nsHtml5TreeOpExecutor::RunFlushLoop > nsJSUtils::EvaluateString` spent `1050 ms`

    ```
    summary/1264535/
    └── Startup::XRE_Main
        ├── nsHtml5TreeOpExecutor::RunFlushLoop
        │   └── nsJSUtils::EvaluateString
        │       └── domLoading_to_loadEventEnd.timeunit
        │           └── 1050.time
    ```

* template
  * Golden templat methods call structure.
