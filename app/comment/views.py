from flask_login import login_required

from app.comment import comment
from app.decorators import permission_required
from app.models import Permission


@comment.route('/upload-comment', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.COMMENT)
def upload_comment():
    pass


@comment.route('/view-all-comments')
@login_required
@permission_required(Permission.VIEW_ALL_COMMENTS)
def view_all():
    pass


@comment.route('/comment-detail')
@login_required
def view_detail():
    pass


@comment.route('/reply-comment', methods=['GET', 'POST'])
@login_required
def reply_comment():
    pass


