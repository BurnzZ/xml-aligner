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

Now press `<leader>a` and see the magic. Just make sure your vim buffer is written to file for the script to read.

## Notes

You can compartmentalize groups of self-closing tags (belonging to the same parent node) with different alignments by having an empty line between them.

#### Example

These two groups would have separate alignments even though they are in the same *parent node*

``` xml
<div id = "main">
    <img src = "#tag1" class = "side main" />
    <img src = "#tag223" class = "side main" />

    <img src = "#here" alt = "placeholder front" class = "side minor" />
    <img src = "#there" alt = "placeholder back" class = "side minor" />
</div>
```
