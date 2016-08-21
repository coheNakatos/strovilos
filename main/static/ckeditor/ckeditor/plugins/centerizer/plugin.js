CKEDITOR.plugins.add('centerizer',
{
    init: function (editor) {
        var pluginName = 'centerizer';
        editor.ui.addButton('Centerizer',
            {
                label: 'Κεντράρισμα Εικόνας',
                command: 'center_image',
                icon: CKEDITOR.plugins.getPath('centerizer') + 'center.png'
            });
        var cmd = editor.addCommand('center_image', { exec: Center });
    }
});
function Center(e) {
    image = e.getSelection().getStartElement();
    if (image.getName() === 'img') {
        curr_styles = image.getAttribute('style');
        new_styles = curr_styles + "display:block; margin:0 auto;";
        image.setAttribute('style', new_styles)
    } 
}