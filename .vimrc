let mapleader = " "
syntax enable 

set nu
set mouse=a
set wrap
set smartindent
set cindent
set relativenumber
set noswapfile
set noerrorbells
set noexpandtab
set tabstop=4
set shiftwidth=4
set foldmethod=indent

packloadall
colorscheme dracula 
nnoremap <leader>v :vsplit<CR>
nnoremap <leader>. <C-W>l
nnoremap <leader>, <C-W>h
nnoremap <leader>k <C-W>k
nnoremap <leader>j <C-W>j

nnoremap <leader>w :wq<CR>
nnoremap <leader>t :vertical terminal<CR>
nnoremap <leader>f :Files<CR>
nnoremap <leader>b :Buffers<CR>
nnoremap <leader>h :FzfInsertFunctionName<CR>
nnoremap <leader>n :NERDTreeToggle<CR>
nnoremap <leader>s :Stdheader<CR>
tnoremap <leader><Esc> <C-\><C-n>
call plug#begin('~/.vim/plugged') " Or '~/.local/share/nvim/plugged' for Neovim

Plug 'preservim/nerdtree'
Plug 'Mofiqul/dracula.nvim'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'davidhalter/jedi-vim'
Plug 'nvie/vim-flake8'

call plug#end()

autocmd BufWritePost *.py call flake8#Flake8()

" Use popup menu (lightweight)
set completeopt=menuone,noinsert,noselect
set pumheight=10

" Jedi settings
let g:jedi#completions_enabled = 1
let g:jedi#popup_on_dot = 1
let g:jedi#show_call_signatures = 2
let g:jedi#auto_vim_configuration = 0
highlight Pmenu      ctermbg=white ctermfg=black
highlight PmenuSel   ctermbg=blue  ctermfg=white
highlight PmenuSbar  ctermbg=grey
highlight PmenuThumb ctermbg=darkgrey
set omnifunc=python3complete#Complete

" Show flake8 message under cursor
function! s:ShowFlake8Message()
    if !exists('b:flake8_loclist')
        return
    endif

    let lnum = line('.')
    for item in b:flake8_loclist
        if item.lnum == lnum
            echohl WarningMsg
            echo item.text
            echohl None
            return
        endif
    endfor
    echo ""
endfunction

" Trigger when cursor stays
set updatetime=300
autocmd CursorHold *.py call <SID>ShowFlake8Message()
let g:flake8_show_quickfix = 0
let g:flake8_show_in_gutter = 1


" ## config
filetype plugin on
