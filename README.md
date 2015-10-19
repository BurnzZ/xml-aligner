## Usage:

```vim
function XMLAlign()
    let cursor = getpos('.')
    let l:winview = winsaveview()
    normal(ggVGd)
    :read !python <path>/xml-aligner.py %
    normal(ggdd)
    call setpos('.', cursor)
    call winrestview(l:winview)
endfunction

map <leader>a :call XMLAlign()<CR>
```
