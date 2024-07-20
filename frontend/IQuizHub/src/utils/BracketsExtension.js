import {Node} from '@tiptap/core'

export default Node.create({
    name: 'brackets',
    priority: 1000,
    inline: true,
    group: 'inline',
    parseHTML() {
        return [
            {
                tag: 'span.brackets'
            }
        ]
    },
    renderHTML({node}) {
        return ['span', {class: 'brackets'}, '()']
    },
    addCommands() {
        return {
            insertBrackets: () => ({chain}) => {
                return chain().insertContent('()').run()
            }
        }
    }
})