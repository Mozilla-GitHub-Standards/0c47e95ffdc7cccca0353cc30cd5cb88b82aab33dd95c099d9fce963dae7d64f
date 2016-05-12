#bugzilla

The folder structure example:

```
.
├── 1269684
│   └── Startup::XRE_Main
│       ├── 836.100
│       ├── Timer::Fire
│       │   └── 177.21.2
│       ├── js::RunScript
│       │   └── 146.17.5
│       ├── nsInputStreamPump::OnInputStreamReady
│       │   ├── 174.20.8
│       │   ├── nsInputStreamPump::OnStateStart
│       │   │   └── 11.1.3
│       │   └── nsInputStreamPump::OnStateStop
│       │       └── 158.18.9
│       └── nsRefreshDriver::Tick
│           ├── 200.23.9
│           ├── PreShell::Flush\ (Flush_InterruptibleLayout)
│           │   └── 22.2.6
│           ├── PreShell::Flush\ (Flush_Style)
│           │   └── 49.5.9
│           ├── PreShell::Paint
│           │   └── 105.12.6
│           └── so\ on
│               └── 0.0
```

The file `177.21.2` means `177 ms` and `21.2 %`.

For more detail, please refer to root folder's [README][ROOT_README].

[ROOT_README]: ../README.md
