import os
import re
from unittest import TestCase

from pygments import lexers
from pygments.token import Token
from vue import lexer as lexer_mod
from vue.lexer import VueLexer

from .tokens_one import TOKENS as expected_tokens_one
from .tokens_two import TOKENS as expected_tokens_two


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


lexer = lexers.load_lexer_from_file(lexer_mod.__file__, "VueLexer")

with open(os.path.join(CURRENT_DIR, 'example_one.vue'), 'r') as fh:
    text_one = fh.read()

with open(os.path.join(CURRENT_DIR, 'example_two.vue'), 'r') as fh:
    text_two = fh.read()


class VueLexerTestCase(TestCase):

    maxDiff = None

    def __filter_tokens(self, tokens):
        space = re.compile('[ \n]+')
        return [i for i in tokens if not space.match (i[1]) and not i[1] == '']

    def test_guess_lexer_for_filename(self):
        guessed_lexer = lexers.guess_lexer_for_filename('test.vue', text_one)
        self.assertEqual(guessed_lexer.name, VueLexer.name)

    def test_get_lexer_by_name(self):
        lexer = lexers.get_lexer_by_name('vue')
        self.assertEqual(lexer.name, VueLexer.name)

    def test_get_tokens_one(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens(text_one)
        self.assertEqual([i for i in tokens], expected_tokens_one)

    def test_get_tokens_two(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens(text_two)
        self.assertEqual([i for i in tokens], expected_tokens_two)

    def test_lexing_directive_one(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <span v-if="book.read">Yes</span>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'span'),
          (Token.Name.Tag, 'v-if='),
          (Token.Literal.String, '"book.read"'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'Yes'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'span'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_two(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <tr v-for="(book, index) in books" :key="index">
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'tr'),
          (Token.Name.Tag, 'v-for='),
          (Token.Literal.String, '"(book, index) in books" :key="index"'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_three(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <span v-else>No</span>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'span'),
          (Token.Name.Tag, 'v-else'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'No'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'span'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_four(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <button type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-update-modal
                    @click="editBook(book)">
                Update
            </button>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'button'),
          (Token.Name.Attribute, 'type'),
          (Token.Operator, '='),
          (Token.Literal.String, '"button"'),
          (Token.Name.Attribute, 'class'),
          (Token.Operator, '='),
          (Token.Literal.String, '"btn btn-warning btn-sm"'),
          (Token.Name.Tag, 'v-b-'),
          (Token.Name.Attribute, 'modal.book'),
          (Token.Name.Tag, '-update'),
          (Token.Name.Tag, '-modal'),
          (Token.Name.Tag, '@click='),
          (Token.Literal.String, '"editBook(book)"'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'Update'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'button'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_five(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <button type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteBook(book)">
                Delete
            </button>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'button'),
          (Token.Name.Attribute, 'type'),
          (Token.Operator, '='),
          (Token.Literal.String, '"button"'),
          (Token.Name.Attribute, 'class'),
          (Token.Operator, '='),
          (Token.Literal.String, '"btn btn-danger btn-sm"'),
          (Token.Name.Tag, '@click='),
          (Token.Literal.String, '"onDeleteBook(book)"'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'Delete'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'button'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_six(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'b'),
          (Token.Name.Tag, '-form'),
          (Token.Name.Tag, '@submit='),
          (Token.Literal.String, '"onSubmit"'),
          (Token.Name.Tag, '@reset='),
          (Token.Literal.String, '"onReset"'),
          (Token.Name.Attribute, 'class'),
          (Token.Operator, '='),
          (Token.Literal.String, '"w-100"'),
          (Token.Punctuation, '>')
        ])


    def test_lexing_directive_seven(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <button class="btn btn-primary btn-block" @click.prevent="validate">Submit</button>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'button'),
          (Token.Name.Attribute, 'class'),
          (Token.Operator, '='),
          (Token.Literal.String, '"btn btn-primary btn-block"'),
          (Token.Name.Tag, '@click.prevent='),
          (Token.Literal.String, '"validate"'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'Submit'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'button'),
          (Token.Punctuation, '>')
        ])

    def test_lexing_directive_eight(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <button class="btn btn-primary btn-block"
                    @click.prevent="validate"
                    :disabled="stripeCheck">
                Submit
            </button>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'button'),
          (Token.Name.Attribute, 'class'),
          (Token.Operator, '='),
          (Token.Literal.String, '"btn btn-primary btn-block"'),
          (Token.Name.Tag, '@click.prevent='),
          (Token.Literal.String, '"validate"'),
          (Token.Name.Tag, ':disabled='),
          (Token.Literal.String, '"stripeCheck"'),
          (Token.Punctuation, '>'),
          (Token.Name.Other, 'Submit'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'button'),
          (Token.Punctuation, '>')
        ])


    def test_lexing_directive_ninet(self):
        lexer = lexers.get_lexer_by_name('vue')
        tokens = lexer.get_tokens('''
            <div v-for="(value, key, index) in object">
              {{ index }}. {{ key }}: {{ value }}
            </div>
        ''')

        self.assertEqual (self.__filter_tokens (tokens), [
          (Token.Punctuation, '<'),
          (Token.Name.Tag, 'div'),
          (Token.Name.Tag, 'v-for='),
          (Token.Literal.String, '"(value, key, index) in object"'),
          (Token.Punctuation, '>'),
          (Token.Punctuation, '{'),
          (Token.Punctuation, '{'),
          (Token.Name.Other, 'index'),
          (Token.Punctuation, '}'),
          (Token.Punctuation, '}'),
          (Token.Punctuation, '.'),
          (Token.Punctuation, '{'),
          (Token.Punctuation, '{'),
          (Token.Name.Other, 'key'),
          (Token.Punctuation, '}'),
          (Token.Punctuation, '}'),
          (Token.Operator, ':'),
          (Token.Punctuation, '{'),
          (Token.Punctuation, '{'),
          (Token.Name.Other, 'value'),
          (Token.Punctuation, '}'),
          (Token.Punctuation, '}'),
          (Token.Punctuation, '<'),
          (Token.Punctuation, '/'),
          (Token.Name.Tag, 'div'),
          (Token.Punctuation, '>')
        ])
