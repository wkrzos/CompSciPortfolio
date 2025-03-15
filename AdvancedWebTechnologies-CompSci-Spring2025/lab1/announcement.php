<?php
/**
 * Plugin Name:       Announcements Plugin
 * Description:       Display of announcements using custom post type
 * Version:           2.0
 * Requires at least: 5.2
 * Requires PHP:      7.2
 * Author:            Igor Podgórniak, Wojciech Krzos
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 **/

function register_announcements_cpt() {
    register_post_type('announcements', [
        'label' => 'Ogłoszenia',
        'public' => true,
        'menu_icon' => 'dashicons-megaphone',
        'supports' => ['title', 'editor', 'custom-fields'],
        'show_in_rest' => true
    ]);
}
add_action('init', 'register_announcements_cpt');


function display_random_announcement($content) {
    if ((is_single() || is_home()) && !is_admin()) {
        $announcements = get_posts([
            'post_type'   => 'announcements',
            'orderby'     => 'rand',
            'numberposts' => 1,
        ]);

        $announcement = $announcements[0];

        if (!empty($announcements)) {
            $ad_content = html_entity_decode($announcement->post_content);
            return "<div>{$ad_content}</div>" . $content;
        }
    }
    return $content;
}
add_filter('the_content', 'display_random_announcement');
