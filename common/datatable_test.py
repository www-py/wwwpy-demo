from common.datatable import Datatable


def test_fieldValue():
    target = new_target()
    assert 'one' == target.rows[0].valueByName('field1')


def test_fieldByName():
    target = new_target()
    assert 'one' == target.rows[0].fieldByName('field1').value
    assert 'field1' == target.rows[0].fieldByName('field1').name.lower()


def test_write():
    target = new_target()
    target.rows[0].fieldByName('field1').value = 'mod1'
    assert target.rows[0].fieldByName('field1').value == 'mod1'
    assert target.rows[0].fieldByName('field1').oldValue == 'one'


def test_delta():
    target = new_target_for_edit()
    target.rows[1].fieldByName('field1').value = 'two-mod'

    update = target.delta()[0]
    assert (1, 'two'), (1, 'two-mod') == update


def test_field_restore_value():
    target = new_target_for_edit()
    target.rows[1].fieldByName('field1').value = 'two-mod'
    target.rows[1].fieldByName('field1').value = 'two'

    update = target.delta()[0]
    assert update == tuple()


def mock_rows():
    return ('field1',), ('one',)


def new_target_for_edit():
    return new_target((('field0', 'field1'), (1, 'one'), (2, 'two')))


def new_target(rows=None):
    if rows is None:
        rows = mock_rows()
    return Datatable(rows)
