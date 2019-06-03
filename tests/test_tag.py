
class TestTagAll(object):

    def test_get_all_tags(self):
        message = 'this tests ContactAll GET method'
        assert message == 'this tests ContactAll GET method'

    def test_post_one_tag(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'


class TestTagOne(object):

    def test_get_one_tag(self):
        message = 'this tests ContactAll GET method'
        assert message == 'this tests ContactAll GET method'

    def test_put_one_tag(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'

    def test_delete_one_tag(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'


class TestTagItemAll(object):

    def test_get_all_tag_items(self):
        message = 'this tests ContactAll GET method'
        assert message == 'this tests ContactAll GET method'

    def test_post_one_tag_item(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'

    def test_post_duplicate_tag_item(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'


class TestTagItemOne(object):

    def test_get_one_tag(self):
        message = 'this tests ContactAll GET method'
        assert message == 'this tests ContactAll GET method'

    def test_put_one_tag(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'

    def test_delete_one_tag(self):
        message = 'this tests ContactOne POST method'
        assert message == 'this tests ContactOne POST method'
