<?php

#
# Valid PHP, just long lines.
#
#

/**
* Set up the Admin Settings menu
*/
function AdminMenu() {
add_options_page(__('Typekit Fonts', 'om4-typekit'), __('Typekit Fonts', 'om4-typekit'), 'manage_options', basename(__FILE__), array(& $this, 'AdminPage'));
}

<div id="error" class="error"><p>
<?php
$instructions = sprintf( __(' Please <a href="%s">click here for instructions</a> on how to obtain your Typekit embed code.', 'om4-typekit'), '#getembedcode');
if (strlen($_POST['embedcode'])) {
// an embed code has been submitted, but was rejected
printf(__('Invalid Typekit embed code. %s', 'om4-typekit'), $instructions);
} else {
// no embed code was submitted
printf(__('You must enter your Typekit embed code. %s', 'om4-typekit'), $instructions);
}
?>
</p></div>
<div id="error" class="error"><p>
<?php printf(__('Your Typekit embed code may be incorrect because  <a href="%1$s" target="_blank">%1$s</a> does not exist. Please verify that your Typekit embed code is correct. If you have just published your kit, please try again in a few minutes.', 'om4-typekit'), $url); ?>
</p></div>
<h2><?php _e('Typekit Fonts for WordPress Settings', 'om4-typekit'); ?></h2>
<p><?php _e('Typekit offer a service that allows you to select from a range of hundreds of high quality fonts for your WordPress website. The fonts are applied using the font-face standard, so they are standards compliant, fully licensed and accessible.', 'om4-typekit'); ?></p>
<li><?php _e('Choose a few fonts to add to your account and Publish them', 'om4-typekit'); ?></li>
<li id="getembedcode"><?php _e('Go to the Kit Editor and get your Embed Code (link at the top right of the screen)', 'om4-typekit'); ?></li>
<li><?php _e('Enter the whole 2 lines of your embed code into the box below.', 'om4-typekit'); ?><br />
<p class="option"><label for="embedcode"><?php _e('Typekit Embed Code:', 'om4-typekit'); ?></label> <textarea name="embedcode" rows="3" cols="80"><?php echo esc_textarea( $this->typekitInstance->GetEmbedCode() ); ?></textarea><br />
<li><?php _e('You can add selectors using the Typekit Kit Editor. Alternatively you can define your own CSS rules in your own style sheet or using the Custom CSS Rules field below (technical note: these CSS rules will be embedded in the header of each page). Look at the advanced examples shown in the Typekit editor for ideas.', 'om4-typekit'); ?>
<p class="option"><label for="css"><?php _e('Custom CSS Rules:', 'om4-typekit'); ?></label> <textarea name="css" rows="10" cols="80"><?php echo esc_textarea( $this->typekitInstance->GetCSSRules() ); ?></textarea><br />
<a href="#help-css"><?php _e('Click here for help on CSS', 'om4-typekit'); ?></a>
<p><?php _e('You can use CSS selectors to apply your new typekit fonts. The settings for this plugin allow you to add new CSS rules to your website to activate Typekit fonts. If you are using fonts for more than just a few elements, you may find it easier to manage this way. And using your own CSS rules is a good way to access different font weights.', 'om4-typekit'); ?></p>
<p><?php _e('There are many options for using CSS, but here are a few common scenarios. Note: we\'ve used proxima-nova for our examples, you\'ll need to change proxima-nova to the name of your chosen font from Typekit - your added font names will be visible in the Kit Editor.', 'om4-typekit'); ?></p>
<p><?php _e('If your Kit contains more than one weight and/or style for a particular font, you need to use numeric <code class="inline">font-weight</code> values in your CSS rules to map to a font\'s weights.', 'om4-typekit'); ?></p>
<p><?php _e('Typekit fonts have been assigned values from 100 to 900 based on information from the font\'s designer. Web browsers also do some guessing as to which weight it should display if the specific value isn\'t present. Say your font has 100, 300 and 900. If you set your text with <code class="inline">font-weight: 400</code>, it will choose the most appropriate (300 in this case).<br />Note: A <code class="inline">font-weight</code> value of 400 corresponds to <code class="inline">font-weight: normal;</code>', 'om4-typekit'); ?></p>
<?php _e('You can target your fonts to specific parts of your website if you know a bit more about your current WordPress theme and where the font family is specified. All WordPress themes have a style.css file, and if you know how to check that you should be able to see the selectors in use. Or you can install Chris Pederick\'s Web Developer Toolbar for Firefox and use the CSS, View CSS option to see all the CSS rules in use for your theme. When you find the selectors that are used for font-family, you can create a rule just for that selector to override that rule.', 'om4-typekit'); ?>
?>
