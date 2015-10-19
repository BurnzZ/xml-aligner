## Usage

`python xml-aligner.py <xml document>[.xml]`

## Hook-up to vim

Add this to your ~/.vimrc:

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

Now press `<leader>a` and see the magic.
