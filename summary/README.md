#summary

The folder structure example:

```
.
├── 1264535.PageDown_3_Page
│   └── Startup::XRE_Main
│       ├── nsHtml5TreeOpExecutor::RunFlushLoop
│       │   └── nsJSUtils::EvaluateString
│       │       └── domLoading_to_loadEventEnd.timeunit
│       │           └── 1050.time
│       ├── nsInputStreamPump::OnInputStreamReady
│       │   └── nsInputStreamPump::OnStateStop
│       │       └── domLoading_to_loadEventEnd.timeunit
│       │           └── 1771.time
│       ├── nsRefreshDriver::Tick
│       │   ├── EventDispatcher::Dispatch
│       │   │   └── PageDown.timeunit
│       │   │       ├── 11.time
│       │   │       └── 58.time
│       │   ├── PresShell::Flush\ (Flush_InterruptibleLayout)
│       │   │   └── domLoading_to_loadEventEnd.timeunit
│       │   │       └── 183.time
│       │   ├── PresShell::Flush\ (Flush_Style)
│       │   │   ├── PageDown.timeunit
│       │   │   │   ├── 21.time
│       │   │   │   └── 21.time.1
│       │   │   └── domLoading_to_loadEventEnd.timeunit
│       │   │       └── 341.time
│       │   ├── PresShell::Paint
│       │   │   ├── PageDown.timeunit
│       │   │   │   ├── 108.time
│       │   │   │   ├── 120.time
│       │   │   │   └── 97.time
│       │   │   └── domLoading_to_loadEventEnd.timeunit
│       │   │       └── 614.time
│       │   └── js::GCRuntime::collect
│       │       └── domLoading_to_loadEventEnd.timeunit
│       │           └── 260.time
│       └── nsViewManager::Dispatch
│           └── EventDispatcher::Dispatch
│               └── PageDown.timeunit
│               └── PageDown.timeunit
│                   ├── 38.time
│                   ├── 44.time
│                   └── 48.time
```

The folder `1264535.PageDown_3_Page` means `Bug 1264535` with the description `PageDown_3_Page`.

The folder `PageDown.timeunit` and `domLoading_to_loadEventEnd.timeunit` means different time unit (action).

The files `<NN>.time` means this time unit (action) spent `<NN> ms`.
If there are more than one results have the same time, the `<NN>.time.1`, `<NN>.time.2` ... etc are accepted.


For more detail, please refer to root folder's [README][ROOT_README].

[ROOT_README]: ../README.md
