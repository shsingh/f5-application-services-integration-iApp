proc iapp_safe_display { args } {
  # strings sent to APL must be truncated to 65535 bytes, see BZ435592
  if { [string length [set [set args]]] > 65535 } {
    set last_newline [string last "\n" [set [set args]] 65500]
    return "[string range [set [set args]] 0 $last_newline]Error: Too many items for display"
  } else {
    return [set [set args]]
  }
}
