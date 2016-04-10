## Usage

`python xml-aligner.py <xml document>[.xml]`

## Hook-up to vim

Clone this to your (preferably to this path):

`git clone https://github.com/BurnzZ/xml-aligner.git ~/.vim/bundle/xml-aligner/`

and add this to your ~/.vimrc:

```vim
function XMLAlign()
    let cursor = getpos('.')
    let l:winview = winsaveview()
    :w
    normal(ggVGd)
    :read !python ~/.vim/bundle/xml-aligner/xml-aligner.py %
    normal(ggdd)
    call setpos('.', cursor)
    call winrestview(l:winview)
endfunction

map <leader>a :call XMLAlign()<CR>
```

Now press `<leader>a` and see the magic.

(*If you've cloned to a different dir other than `~/.vim/bundles/`, make sure you update the path script in the code block above.*)

## Notes

You can compartmentalize groups of self-closing tags (belonging to the same parent node) with different alignments by having an empty line between them.

#### Example

BEFORE:
``` xml
<div id = "main">
    <img src = "#tag1"   class = "side main" />
    <img src = "#tag223" class = "side main" />

    <img src = "#here" class = "side minor" />
    <img src = "#there"      class = "side minor" />
</div>
```

AFTER:
``` xml
<div id = "main">
    <img src = "#tag1"   class = "side main"  />
    <img src = "#tag223" class = "side main"  />

    <img src = "#here"   class = "side minor" />
    <img src = "#there"  class = "side minor" />
</div>
```
