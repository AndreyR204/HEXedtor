#HEXeditor
HEX редактор на Python
##Install
git clone https://github.com/AndreyR204/HEXedtor.git 

pip install -r requirements.txt

##Usage
python -m hex -f "path/to/file"


    arrow keys - movement
    pageup/pagedown - move entire pages
    [0123456789abcdef] - edit the current byte
    shift + q - quit
    shift + w - save file to disk
    '[' ']' - increase/decrease word size
    { } - decrease/increase display width
    p - toggle little endian
    i - toggle insert mode
    DEL - delete previous byte/word
    ESC - switch to text mode
