<?php
#
#
# File with valid PHP and no long lines. Should not trigger rosti.
#
#

/**
* Retrieve the author of the current comment.
*
* If the comment has an empty comment_author field, then 'Anonymous' person is
* assumed.
*
* @since 1.5.0
* @uses apply_filters() Calls 'get_comment_author' hook on the comment author
*
* @param int $comment_ID The ID of the comment for which to retrieve the author. Optional.
* @return string The comment author
*/
function get_comment_author( $comment_ID = 0 ) {
$comment = get_comment( $comment_ID );
if ( empty($comment->comment_author) ) {
if (!empty($comment->user_id)){
$user=get_userdata($comment->user_id);
$author=$user->user_login;
} else {
$author = __('Anonymous');
}
} else {
$author = $comment->comment_author;
}
return apply_filters('get_comment_author', $author);
}

$fields =  array(
'author' => '<p class="comment-form-author">' . '<label for="author">' . __( 'Name' ) . '</label> ' . ( $req ? '<span class="required">*</span>' : '' ) .
'<input id="author" name="author" type="text" value="' . esc_attr( $commenter['comment_author'] ) . '" size="30"' . $aria_req . ' /></p>',
'email'  => '<p class="comment-form-email"><label for="email">' . __( 'Email' ) . '</label> ' . ( $req ? '<span class="required">*</span>' : '' ) .
'<input id="email" name="email" type="text" value="' . esc_attr(  $commenter['comment_author_email'] ) . '" size="30"' . $aria_req . ' /></p>',
'url'    => '<p class="comment-form-url"><label for="url">' . __( 'Website' ) . '</label>' .
'<input id="url" name="url" type="text" value="' . esc_attr( $commenter['comment_author_url'] ) . '" size="30" /></p>',
);

$required_text = sprintf( ' ' . __('Required fields are marked %s'), '<span class="required">*</span>' );
$defaults = array(
'fields'               => apply_filters( 'comment_form_default_fields', $fields ),
'comment_field'        => '<p class="comment-form-comment"><label for="comment">' . _x( 'Comment', 'noun' ) . '</label><textarea id="comment" name="comment" cols="45" rows="8" aria-required="true"></textarea></p>',
'must_log_in'          => '<p class="must-log-in">' .  sprintf( __( 'You must be <a href="%s">logged in</a> to post a comment.' ), wp_login_url( apply_filters( 'the_permalink', get_permalink( $post_id ) ) ) ) . '</p>',
'logged_in_as'         => '<p class="logged-in-as">' . sprintf( __( 'Logged in as <a href="%1$s">%2$s</a>. <a href="%3$s" title="Log out of this account">Log out?</a>' ), admin_url( 'profile.php' ), $user_identity, wp_logout_url( apply_filters( 'the_permalink', get_permalink( $post_id ) ) ) ) . '</p>',
'comment_notes_before' => '<p class="comment-notes">' . __( 'Your email address will not be published.' ) . ( $req ? $required_text : '' ) . '</p>',
'comment_notes_after'  => '<p class="form-allowed-tags">' . sprintf( __( 'You may use these <abbr title="HyperText Markup Language">HTML</abbr> tags and attributes: %s' ), ' <code>' . allowed_tags() . '</code>' ) . '</p>'
?>
